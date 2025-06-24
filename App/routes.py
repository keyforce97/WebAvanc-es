from flask import Blueprint, jsonify, request, redirect, url_for, render_template
from peewee import DoesNotExist 
from App.models import Order, DoesNotExist
from .models import Product, Order
import json 
import requests

# Définition du Blueprint
bp = Blueprint('routes', __name__)

# ---------------------------------
# GET / - Liste des produits
# ---------------------------------
@bp.route('/', methods=['GET'])
def get_products():
    products = []
    for product in Product.select():
        products.append({
            "name": product.name,
            "id": product.id,
            "in_stock": product.in_stock,
            "description": product.description,
            "price": product.price,
            "weight": product.weight,
            "image": product.image
        })
    return jsonify({"products": products}), 200

# ---------------------------------
# POST /order - Créer une commande
# ---------------------------------
@bp.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    # On accepte 'products' (liste) ou 'product' (rétrocompatibilité)
    products = data.get('products')
    if not products:
        # Rétrocompatibilité : un seul produit
        product = data.get('product')
        if not product:
            return jsonify({
                "errors": {"product": {"code": "missing-fields", "name": "Aucun produit fourni"}}
            }), 422
        products = [product]
    # Vérification des produits
    order_products = []
    total_price = 0
    total_weight = 0
    for p in products:
        if 'id' not in p or 'quantity' not in p or p['quantity'] < 1:
            return jsonify({
                "errors": {"product": {"code": "missing-fields", "name": "Produit ou quantité manquante"}}
            }), 422
        try:
            prod = Product.get(Product.id == p['id'])
        except DoesNotExist:
            return jsonify({
                "errors": {"product": {"code": "not-found", "name": f"Produit {p['id']} introuvable"}}
            }), 422
        if not prod.in_stock:
            return jsonify({
                "errors": {"product": {"code": "out-of-inventory", "name": f"Produit {p['id']} hors stock"}}
            }), 422
        order_products.append((prod, p['quantity']))
        total_price += prod.price * p['quantity']
        total_weight += prod.weight * p['quantity']
    # Calcul du shipping
    if total_weight <= 500:
        shipping_price = 500
    elif total_weight <= 2000:
        shipping_price = 1000
    else:
        shipping_price = 2500
    # Création de la commande
    order = Order.create(
        shipping_price=shipping_price,
        total_price=total_price,
        paid=False
    )
    # Ajout des produits à la commande
    from .models import OrderProduct
    for prod, qty in order_products:
        OrderProduct.create(order=order, product=prod, quantity=qty)
    return redirect(url_for('routes.get_order', order_id=order.id), code=302)

def is_payment_in_progress(redis_client, order_id):
    return redis_client.get(f'order:{order_id}:paying')

@bp.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    from .redis_client import redis_client
    import json
    # Vérifier si paiement en cours (flag Redis)
    if is_payment_in_progress(redis_client, order_id):
        return '', 202
    # Vérifier d'abord dans Redis
    cached = redis_client.get(f'order:{order_id}')
    if cached:
        order_data = json.loads(cached)
        return jsonify({"order": order_data}), 200
    # Sinon, lire dans la base
    try:
        order = Order.get(Order.id == order_id)
    except DoesNotExist:
        return jsonify({"errors": {"order": {"code": "not-found", "name": "La commande n'existe pas"}}}), 404
    # Récupérer les produits
    from .models import OrderProduct
    products = [
        {"id": op.product.id, "quantity": op.quantity}
        for op in OrderProduct.select().where(OrderProduct.order == order)
    ]
    shipping_info = json.loads(order.shipping_information) if order.shipping_information else {}
    credit_card = json.loads(order.credit_card) if order.credit_card else {}
    transaction = json.loads(order.transaction) if order.transaction else {}
    response = {
        "order": {
            "id": order.id,
            "total_price": order.total_price,
            "email": order.email,
            "credit_card": credit_card if order.paid else {},
            "shipping_information": shipping_info,
            "paid": order.paid,
            "transaction": transaction if order.paid else {},
            "products": products,
            "shipping_price": order.shipping_price
        }
    }
    return jsonify(response), 200

@bp.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Met à jour la commande (email, shipping) et lance le paiement en tâche de fond si credit_card présent.
    Retourne 202 si paiement en cours, 409 si déjà payé, 200 sinon.
    """
    from .models import OrderProduct
    from .services import process_payment
    from .redis_client import redis_client
    from rq import Queue
    import json
    data = request.get_json()
    if not data:
        return jsonify({"errors": {"order": {"code": "missing-fields", "name": "Aucune donnée reçue"}}}), 422
    # Récupérer la commande
    try:
        order = Order.get(Order.id == order_id)
    except DoesNotExist:
        return jsonify({"errors": {"order": {"code": "not-found", "name": "La commande n'existe pas"}}}), 404
    # Si déjà payée, on ne peut plus modifier
    if order.paid:
        return '', 409
    # Si paiement en cours (vérifier le flag Redis)
    if is_payment_in_progress(redis_client, order_id):
        return '', 202
    # Mettre à jour email et shipping si présents
    email = data.get('email')
    shipping_info = data.get('shipping_information')
    if email:
        order.email = email
    if shipping_info:
        order.shipping_information = json.dumps(shipping_info)
    # Recalculer prix total et shipping
    products = OrderProduct.select().where(OrderProduct.order == order)
    total_price = sum(op.product.price * op.quantity for op in products)
    total_weight = sum(op.product.weight * op.quantity for op in products)
    if total_weight <= 500:
        shipping_price = 500
    elif total_weight <= 2000:
        shipping_price = 1000
    else:
        shipping_price = 2500
    order.total_price = total_price
    order.shipping_price = shipping_price
    # Calcul taxe selon la province
    province = shipping_info['province'] if shipping_info and 'province' in shipping_info else ''
    tax_rates = {"QC": 0.15, "ON": 0.13, "AB": 0.05, "BC": 0.12, "NS": 0.14}
    tax_rate = tax_rates.get(province, 0)
    order.total_price_tax = round(total_price * (1 + tax_rate), 2)
    order.save()
    # Si credit_card présent, lancer le paiement en tâche de fond
    credit_card = data.get('credit_card')
    if credit_card:
        # On peut marquer la commande comme "en cours de paiement" (champ à ajouter si besoin)
        # Lancer la tâche RQ
        q = Queue(connection=redis_client)
        q.enqueue(process_payment, order.id, credit_card)
        return '', 202
    # Sinon, retour normal
    response = {
        "order": {
            "id": order.id,
            "email": order.email,
            "shipping_information": json.loads(order.shipping_information) if order.shipping_information else {},
            "credit_card": {},
            "paid": order.paid,
            "transaction": {},
            "products": [
                {"id": op.product.id, "quantity": op.quantity} for op in products
            ],
            "shipping_price": order.shipping_price,
            "total_price": order.total_price,
            "total_price_tax": order.total_price_tax
        }
    }
    return jsonify(response), 200

# La route /order/<order_id>/pay n'est plus nécessaire car le paiement se fait via PUT /order/<order_id>
# On la retire pour éviter toute confusion.

@bp.route('/test', methods=['GET'])
def test_page():
    return render_template('index.html')
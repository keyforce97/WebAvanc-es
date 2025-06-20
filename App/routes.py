from flask import Blueprint, jsonify, request, redirect, url_for
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
 
    # Vérifie si "product" est présent
    if not data or 'product' not in data:
        return jsonify({
            "errors": {
                "product": {
                    "code": "missing-fields",
                    "name": "La création d'une commande nécessite un produit 1"
                }
            }
        }), 422

    product_data = data['product']

    # Vérifie la présence des champs 'id' et 'quantity'
    if 'id' not in product_data or 'quantity' not in product_data:
        return jsonify({
            "errors": {
                "product": {
                    "code": "missing-fields",
                    "name": "La création d'une commande nécessite un produit 2"
                }
            }
        }), 422

    product_id = product_data['id']
    quantity = product_data['quantity']
    
    
    if quantity < 1:
        return jsonify({
            "errors": {
                "product": {
                    "code": "missing-fields",
                    "name": "La quantité doit être supérieure ou égale à 1"
                }
            }
        }), 422

    # Vérifie si le produit existe
    try:
        product = Product.get(Product.id == product_id)
    except DoesNotExist:
        return jsonify({
            "errors": {
                "product": {
                    "code": "not-found",
                    "name": "Le produit demandé n'existe pas"
                }
            }
        }), 422

    # Vérifie si le produit est en stock
    if not product.in_stock:
        return jsonify({
            "errors": {
                "product": {
                    "code": "out-of-inventory",
                    "name": "Le produit demandé n'est pas en inventaire"
                }
            }
        }), 422

    # Crée la commande
    order = Order.create(
        product_id=product.id,
        quantity=quantity
    )

    return redirect(url_for('routes.get_order', order_id=order.id), code=302)

@bp.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = Order.get(Order.id == order_id)
        response = {
            "order": {
                "id": order.id,
                "total_price": order.total_price,
                "total_price_tax": order.total_price_tax,
                "email": order.email,
                "credit_card": {},
                "shipping_information": {},
                "paid": order.paid,
                "transaction": {},
                "product": {
                    "id": order.product_id,
                    "quantity": order.quantity
                },
                "shipping_price": order.shipping_price
            }
        }
        return jsonify(response), 200
    except DoesNotExist:
        return jsonify({
            "errors": {
                "order": {
                    "code": "not-found",
                    "name": "La commande n'existe pas"
                }
            }
        }), 404

@bp.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    if not data or 'order' not in data:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires 4"
                }
            }
        }), 422

    order_data = data['order']
    required_fields = ['email', 'shipping_information']
    shipping_required = ['country', 'address', 'postal_code', 'city', 'province']

    # Vérifie les champs requis
    for field in required_fields:
        if field not in order_data:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires 3"
                    }
                }
            }), 422

    shipping_info = order_data['shipping_information']
    for field in shipping_required:
        if field not in shipping_info:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires 5"
                    }
                }
            }), 422

    try:
        order = Order.get(Order.id == order_id)
    except DoesNotExist:
        return jsonify({
            "errors": {
                "order": {
                    "code": "not-found",
                    "name": "La commande n'existe pas"
                }
            }
        }), 404

    # Calcul des prix
    product = Product.get(Product.id == order.product_id)
    total_price = product.price * order.quantity

    # Calcul shipping
    weight = product.weight * order.quantity
    if weight <= 500:
        shipping_price = 500
    elif weight <= 2000:
        shipping_price = 1000
    else:
        shipping_price = 2500

    # Calcul taxe selon la province
    province = shipping_info['province']
    tax_rates = {"QC": 0.15, "ON": 0.13, "AB": 0.05, "BC": 0.12, "NS": 0.14}
    tax_rate = tax_rates.get(province, 0)
    total_price_tax = round(total_price * (1 + tax_rate), 2)

    # Mise à jour de la commande
    order.email = order_data['email']
    order.shipping_information = json.dumps(shipping_info)
    order.shipping_price = shipping_price
    order.total_price = total_price
    order.total_price_tax = total_price_tax
    order.save()

    # Retourner la commande mise à jour
    response = {
        "order": {
            "id": order.id,
            "email": order.email,
            "shipping_information": shipping_info,
            "credit_card": {},
            "paid": order.paid,
            "transaction": {},
            "product": {
                "id": order.product_id,
                "quantity": order.quantity
            },
            "shipping_price": shipping_price,
            "total_price": total_price,
            "total_price_tax": total_price_tax
        }
    }

    return jsonify(response), 200


# ---------------------------------
# PUT / - Paiement
# ---------------------------------
@bp.route('/order/<int:order_id>/pay', methods=['PUT'])
def pay_order(order_id):
    import json
    from flask import request, jsonify
    from App.models import Order, DoesNotExist
    import requests

    data = request.get_json()

    # Vérification du JSON reçu
    if not data or 'credit_card' not in data:
        return jsonify({
            "errors": {
                "order": {
                    "code": "missing-fields",
                    "name": "Il manque un ou plusieurs champs qui sont obligatoires"
                }
            }
        }), 422

    credit_card = data['credit_card']
    required_fields = ['name', 'number', 'expiration_year', 'expiration_month', 'cvv']

    for field in required_fields:
        if field not in credit_card:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "missing-fields",
                        "name": "Il manque un ou plusieurs champs qui sont obligatoires"
                    }
                }
            }), 422

    try:
        order = Order.get(Order.id == order_id)
    except DoesNotExist:
        return jsonify({
            "errors": {
                "order": {
                    "code": "not-found",
                    "name": "La commande n'existe pas"
                }
            }
        }), 404

    if order.paid:
        return jsonify({
            "errors": {
                "order": {
                    "code": "already-paid",
                    "name": "La commande est déjà payée"
                }
            }
        }), 422

    # Construire la requête à envoyer à l'API externe
    payload = {
        "credit_card": {
            "name": credit_card["name"],
            "number": credit_card["number"],
            "expiration_year": int(credit_card["expiration_year"]),
            "cvv": credit_card["cvv"],
            "expiration_month": int(credit_card["expiration_month"])
        },
        "amount_charged": order.total_price_tax + order.shipping_price
    }

    print("Payload envoyé à l'API externe :", json.dumps(payload, indent=2))

    try:
        response = requests.post("https://dimensweb.uqac.ca/~jgnault/shops/pay/", json=payload)
        result = response.json()
        print("Réponse brute API externe :", json.dumps(result, indent=2))

        if response.status_code != 200:
            return jsonify({
                "errors": {
                    "order": {
                        "code": "payment-failed",
                        "name": "Erreur lors du paiement"
                    }
                }
            }), 422

        if "errors" in result:
            return jsonify({
                "errors": {
                    "order": {
                        "code": result['errors']['credit_card']['code'],
                        "name": result['errors']['credit_card']['name']
                    }
                }
            }), 422

        # Mettre à jour la commande
        order.paid = True
        order.credit_card = json.dumps(result['credit_card'])
        order.transaction = json.dumps(result['transaction'])
        order.save()

        response_data = {
            "order": {
                "id": order.id,
                "email": order.email,
                "shipping_information": json.loads(order.shipping_information),
                "credit_card": result['credit_card'],
                "transaction": result['transaction'],
                "product": {
                    "id": order.product_id,
                    "quantity": order.quantity
                },
                "shipping_price": order.shipping_price,
                "total_price": order.total_price,
                "total_price_tax": order.total_price_tax,
                "paid": order.paid
            }
        }

        return jsonify(response_data), 200

    except Exception as e:
        print("Erreur inattendue :", str(e))
        return jsonify({
            "errors": {
                "order": {
                    "code": "payment-failed",
                    "name": "Erreur inattendue lors du paiement"
                }
            }
        }), 422

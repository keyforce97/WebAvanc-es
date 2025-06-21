import requests
from .models import Product, db, Order, OrderProduct
from .redis_client import redis_client
import json

def fetch_and_store_products():
    url = "http://dimensweb.uqac.ca/~jgnault/shops/products/"
    response = requests.get(url)
    if response.status_code == 200:
        products = response.json().get("products", [])
        with db.atomic():
            for p in products:
                Product.create(
                    id=p["id"],
                    name=p["name"],
                    description=p["description"],
                    price=p["price"],
                    in_stock=p["in_stock"],
                    weight=p["weight"],
                    image=p["image"]
                )
        print(f"{len(products)} produits importés avec succès !")
    else:
        print("Erreur lors de la récupération des produits.")

def process_payment(order_id, credit_card):
    """
    Fonction appelée par RQ pour traiter le paiement d'une commande.
    - Met à jour la commande comme payée
    - Met la commande en cache dans Redis
    - Gère le statut "en cours de paiement" via Redis
    - Gère les erreurs de paiement (simulation ou appel réel)
    """
    # Marquer la commande comme "en cours de paiement" dans Redis
    redis_client.set(f'order:{order_id}:paying', '1')
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        redis_client.delete(f'order:{order_id}:paying')
        return
    # Simuler un appel à un service de paiement externe (ici, succès)
    try:
        # Ici, tu pourrais faire un vrai appel HTTP si besoin
        # Simuler une réussite
        transaction = {
            'id': 'transaction_id',
            'success': True,
            'error': {},
            'amount_charged': order.total_price + order.shipping_price
        }
        credit_card_info = {
            'name': credit_card.get('name'),
            'first_digits': str(credit_card.get('number', ''))[:4],
            'last_digits': str(credit_card.get('number', ''))[-4:],
            'expiration_year': credit_card.get('expiration_year'),
            'expiration_month': credit_card.get('expiration_month')
        }
        order.paid = True
        order.credit_card = json.dumps(credit_card_info)
        order.transaction = json.dumps(transaction)
        order.save()
    except Exception as e:
        # En cas d'erreur, stocker l'erreur dans transaction
        transaction = {
            'id': 'transaction_id',
            'success': False,
            'error': {'code': 'payment-error', 'name': str(e)},
            'amount_charged': order.total_price + order.shipping_price
        }
        order.paid = False
        order.transaction = json.dumps(transaction)
        order.save()
    # Mettre la commande en cache Redis
    order_data = {
        'id': order.id,
        'total_price': order.total_price,
        'shipping_price': order.shipping_price,
        'email': order.email,
        'credit_card': json.loads(order.credit_card) if order.credit_card else {},
        'shipping_information': json.loads(order.shipping_information) if order.shipping_information else {},
        'paid': order.paid,
        'transaction': json.loads(order.transaction) if order.transaction else {},
        'products': [
            {'id': op.product.id, 'quantity': op.quantity}
            for op in OrderProduct.select().where(OrderProduct.order == order)
        ]
    }
    redis_client.set(f'order:{order.id}', json.dumps(order_data))
    # Supprimer le flag "en cours de paiement"
    redis_client.delete(f'order:{order_id}:paying')

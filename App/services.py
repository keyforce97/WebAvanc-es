import requests
import time
from .models import Product, db, Order, OrderProduct
from .redis_client import redis_client
import json

def clean_text(text):
    if isinstance(text, str):
        return text.replace('\x00', '').replace('\u0000', '').replace(chr(0), '')
    return text

def fetch_and_store_products():
    url = "http://dimensweb.uqac.ca/~jgnault/shops/products/"
    response = requests.get(url)
    if response.status_code == 200:
        products = response.json().get("products", [])
        with db.atomic():
            for p in products:
                Product.get_or_create(
                    id=p["id"],
                    defaults={
                        "name":        clean_text(p["name"]),
                        "description": clean_text(p["description"]),
                        "price":       p["price"],
                        "in_stock":    p["in_stock"],
                        "weight":      p["weight"],
                        "image":       clean_text(p["image"]),
                    }
                )
        print(f"{len(products)} produits importés ou mis à jour avec succès !")
    else:
        print("Erreur lors de la récupération des produits.")

def process_payment(order_id, credit_card):
    print(f"[WORKER] Début process_payment pour order_id={order_id}")
    # Marquer la commande comme "en cours de paiement" dans Redis
    redis_client.set(f'order:{order_id}:paying', '1')
    order = Order.get_or_none(Order.id == order_id)
    if not order:
        print(f"[WORKER] Order {order_id} introuvable !")
        redis_client.delete(f'order:{order_id}:paying')
        return
    
    # Validation des données de carte
    card_number = str(credit_card.get('number', ''))
    card_name = credit_card.get('name', '').strip()
    expiry_year = credit_card.get('expiration_year')
    expiry_month = credit_card.get('expiration_month')
    
    if not card_number or len(card_number) < 13 or len(card_number) > 19:
        print(f"[WORKER] Numéro de carte invalide pour order_id={order_id}")
        redis_client.delete(f'order:{order_id}:paying')
        return
        
    if not card_name or len(card_name) < 2:
        print(f"[WORKER] Nom de carte invalide pour order_id={order_id}")
        redis_client.delete(f'order:{order_id}:paying')
        return
    
    try:
        print(f"[WORKER] Paiement simulé pour order_id={order_id}")
        
        # Simulation d'appel au service de paiement avec URL réelle
        payment_data = {
            'credit_card': {
                'name': card_name,
                'number': card_number,
                'expiration_year': expiry_year,
                'expiration_month': expiry_month,
                'cvv': credit_card.get('cvv', '')
            },
            'amount_charged': int((order.total_price_tax + (order.shipping_price / 100)) * 100)  # En centimes
        }
        
        # Appel vers le service de paiement
        try:
            response = requests.post(
                "http://dimprojetu.uqac.ca/~jgnault/shops/pay/",
                json=payment_data,
                timeout=30
            )
            response.raise_for_status()
            payment_result = response.json()
            
            if payment_result.get('transaction', {}).get('success', False):
                # Paiement réussi
                transaction = payment_result['transaction']
                # Stockage sécurisé - JAMAIS le numéro complet
                credit_card_info = {
                    'name': card_name,
                    'first_digits': card_number[:4],
                    'last_digits': card_number[-4:],
                    'expiration_year': expiry_year,
                    'expiration_month': expiry_month
                }
                
                order.paid = True
                order.credit_card = json.dumps(credit_card_info)
                order.transaction = json.dumps(transaction)
                order.save()
                print(f"[WORKER] Paiement réussi pour order_id={order_id}")
            else:
                # Paiement échoué (erreur métier)
                transaction = payment_result.get('transaction', {})
                order.paid = False
                order.credit_card = json.dumps({})  # Pas de stockage en cas d'échec
                order.transaction = json.dumps(transaction)
                order.save()
                print(f"[WORKER] Paiement échoué pour order_id={order_id}: {transaction.get('error', {})}")
                
        except requests.RequestException as e:
            # Erreur de communication avec le service
            print(f"[WORKER] Erreur de communication avec le service de paiement pour order_id={order_id} : {e}")
            transaction = {
                'id': f'txn_error_{order_id}_{int(time.time())}',
                'success': False,
                'error': {'code': 'service-unavailable', 'name': 'Service de paiement indisponible'},
                'amount_charged': int((order.total_price_tax + (order.shipping_price / 100)) * 100)
            }
            order.paid = False
            order.credit_card = json.dumps({})
            order.transaction = json.dumps(transaction)
            order.save()
        
    except Exception as e:
        print(f"[WORKER] Erreur générale paiement pour order_id={order_id} : {e}")
        # En cas d'erreur générale
        transaction = {
            'id': f'txn_error_{order_id}_{int(time.time())}',
            'success': False,
            'error': {'code': 'internal-error', 'name': str(e)},
            'amount_charged': int((order.total_price_tax + (order.shipping_price / 100)) * 100)
        }
        order.paid = False
        order.credit_card = json.dumps({})
        order.transaction = json.dumps(transaction)
        order.save()
    # Mettre la commande en cache Redis
    order_data = {
        'id': order.id,
        'total_price': order.total_price,
        'total_price_tax': order.total_price_tax,
        'shipping_price': order.shipping_price,
        'email': order.email,
        'credit_card': json.loads(order.credit_card) if order.credit_card else {},
        'shipping_information': json.loads(order.shipping_information) if order.shipping_information else {},
        'paid': order.paid,
        'order_status': 'paid' if order.paid else 'unpaid',
        'transaction': json.loads(order.transaction) if order.transaction else {},
        'products': [
            {'id': op.product.id, 'quantity': op.quantity}
            for op in OrderProduct.select().where(OrderProduct.order == order)
        ]
    }
    redis_client.set(f'order:{order.id}', json.dumps(order_data))
    print(f"[WORKER] Commande {order_id} mise à jour dans Redis.")
    # Supprimer le flag "en cours de paiement"
    redis_client.delete(f'order:{order_id}:paying')
    print(f"[WORKER] Fin process_payment pour order_id={order_id}")

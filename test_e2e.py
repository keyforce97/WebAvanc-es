import requests
import time

API_URL = "http://localhost:5002"

def wait_for_api(timeout=60):
    print("Attente du démarrage de l'API...")
    for _ in range(timeout):
        try:
            r = requests.get(f"{API_URL}/")
            if r.status_code == 200:
                print("API disponible !")
                return True
        except Exception:
            pass
        time.sleep(1)
    print("L'API n'a pas démarré à temps.")
    return False

def test_achat():
    # 1. Récupérer la liste des produits
    r = requests.get(f"{API_URL}/")
    assert r.status_code == 200, "Erreur récupération produits"
    produits = r.json()
    assert produits, "Aucun produit trouvé"
    prod = produits[0]
    print(f"Produit choisi : {prod}")

    # 2. Créer une commande
    order_payload = {
        "email": "test@uqac.ca",
        "shipping_information": {
            "address": "123 rue Test",
            "city": "Chicoutimi",
            "postal_code": "G7H1Z1"
        },
        "products": [
            {"id": prod["id"], "quantity": 1}
        ]
    }
    r = requests.post(f"{API_URL}/order", json=order_payload)
    assert r.status_code == 201, f"Erreur création commande: {r.text}"
    order = r.json()
    print(f"Commande créée : {order['id']}")

    # 3. Payer la commande
    pay_payload = {
        "credit_card": {
            "name": "Test User",
            "number": "4242424242424242",
            "expiration_year": 2030,
            "expiration_month": 12
        }
    }
    r = requests.put(f"{API_URL}/order/{order['id']}", json=pay_payload)
    assert r.status_code == 200, f"Erreur paiement: {r.text}"
    print("Paiement effectué.")

    # 4. Vérifier la commande payée
    time.sleep(2)  # Laisser le worker traiter le paiement si asynchrone
    r = requests.get(f"{API_URL}/order/{order['id']}")
    assert r.status_code == 200, "Erreur récupération commande"
    commande = r.json()
    assert commande["paid"] is True, "La commande n'est pas marquée comme payée"
    print("Test d'achat réussi !")

if __name__ == "__main__":
    if wait_for_api():
        test_achat()
    else:
        print("Impossible de tester l'achat, API indisponible.")
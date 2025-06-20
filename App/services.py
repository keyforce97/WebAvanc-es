import requests
from .models import Product, db

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

from peewee import *
import os
from playhouse.postgres_ext import PostgresqlExtDatabase

# variables pour connexion PostgreSQL
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'pass') 
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'database')

# Connexion à la base PostgreSQL
db = PostgresqlExtDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

class BaseModel(Model):
    class Meta:
        database = db

class Product(BaseModel):
    id          = IntegerField(primary_key=True)
    name        = CharField()
    description = TextField()
    price       = FloatField()
    in_stock    = BooleanField()
    weight      = IntegerField()
    image       = CharField()

# La table Order représente une commande par un utilisateur.
# Chaque commande peut contenir plusieurs produits via la table OrderProduct.
class Order(BaseModel):
    id                   = AutoField()
    email                = CharField(null=True)
    shipping_information = TextField(null=True)
    paid                 = BooleanField(default=False)
    shipping_price       = IntegerField(default=0)
    total_price          = FloatField(default=0.0)
    total_price_tax      = FloatField(default=0.0)
    credit_card          = TextField(null=True)
    transaction          = TextField(null=True)

class OrderProduct(BaseModel):
    """
    Table de liaison pour gérer plsuieurs produits en une seule commande.
    Chaque ligne représente un produit dans une commande avec sa quantité.
    """
    id       = AutoField()
    order    = ForeignKeyField(Order, backref='order_products')
    product  = ForeignKeyField(Product)
    quantity = IntegerField(default=1)

from peewee import (
    Model, AutoField, IntegerField, CharField, TextField,
    FloatField, BooleanField, ForeignKeyField
)
from .config import DB

class BaseModel(Model):
    class Meta:
        database = DB

class Product(BaseModel):
    id          = IntegerField(primary_key=True)
    name        = CharField()
    description = TextField()
    price       = FloatField()
    in_stock    = BooleanField()
    weight      = IntegerField()
    image       = CharField()

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
    Table de liaison pour gérer N produits → 1 commande.
    """
    id       = AutoField()
    order    = ForeignKeyField(Order, backref='order_products')
    product  = ForeignKeyField(Product)
    quantity = IntegerField(default=1)

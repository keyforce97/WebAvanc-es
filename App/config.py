import os
from peewee import PostgresqlDatabase

DB = PostgresqlDatabase(
    os.getenv("DB_NAME"),
    user    = os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    host    = os.getenv("DB_HOST"),
    port    = int(os.getenv("DB_PORT", 5432)),
)
REDIS_URL = os.getenv("REDIS_URL")



#jeusis 
from fastapi import FastAPI
from typing import List
import random
import json
import pandas as pd
from faker import Faker

app = FastAPI()
fake = Faker()
languages = ['en', 'es', 'fr', 'de', 'it', 'jp', 'kr', 'cn', 'ru', 'pt']

def generate_custom_field():
    base_keys = [
        ("nivel", lambda: random.randint(1, 100)),
        ("poder", lambda: random.choice(["fuego", "agua", "trueno", "tierra", None])),
        ("activo", lambda: random.choice([True, False])),
        ("inventario", lambda: random.sample(["espada", "escudo", "poción", "llave", "oro"], k=random.randint(1, 4))),
        ("aliado", lambda: fake.first_name() if random.random() > 0.5 else None),
        ("misiones_completadas", lambda: random.randint(0, 50)),
        ("atributos", lambda: {"fuerza": random.randint(1, 10), "agilidad": random.uniform(1.0, 10.0)}),
        ("comentario", lambda: fake.sentence(nb_words=6)),
        ("puntos", lambda: random.choice([None, random.randint(0, 1000)])),
        ("historial", lambda: [{"fecha": fake.date(), "evento": fake.word()} for _ in range(random.randint(1, 3))])
    ]
    keys_to_include = random.sample(base_keys, k=random.randint(2, 6))
    return {key: generator() for key, generator in keys_to_include}

def generate_user_records(n=1000):
    records = []
    for _ in range(n):
        name = fake.first_name()
        surname = fake.last_name()
        lang = random.choice(languages)
        telephone = fake.msisdn()[0:9]
        email = f"{name.lower()}.{surname.lower()}@{fake.free_email_domain()}"
        username = f"{name.lower()}{random.randint(1, 999)}"
        custom = generate_custom_field()
        records.append({
            "name": name,
            "surname": surname,
            "ow_lang": lang,
            "telephone": telephone,
            "email": email,
            "username": username,
            "custom": custom
        })
    return records

@app.get("/fake-data")
def get_fake_data(count: int = 1000) -> List[dict]:
    return generate_user_records(count)
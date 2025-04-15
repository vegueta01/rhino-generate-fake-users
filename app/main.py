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
        ("aliado", lambda: generate_full_name() if random.random() > 0.5 else None),
        ("misiones_completadas", lambda: random.randint(0, 50)),
        ("atributos", lambda: {"fuerza": random.randint(1, 10), "agilidad": random.uniform(1.0, 10.0)}),
        ("comentario", lambda: fake.sentence(nb_words=6)),
        ("puntos", lambda: random.choice([None, random.randint(0, 1000)])),
        ("historial", lambda: [{"fecha": fake.date(), "evento": fake.word()} for _ in range(random.randint(1, 3))])
    ]
    keys_to_include = random.sample(base_keys, k=random.randint(2, 6))
    return {key: generator() for key, generator in keys_to_include}

def generate_full_name():
    """Genera un nombre compuesto con probabilidad"""
    if random.random() < 0.3:  # 30% probabilidad de tener nombre compuesto
        return f"{fake.first_name()} {fake.first_name()}"
    return fake.first_name()

def generate_full_surname():
    """Genera apellidos compuestos con probabilidad según diferentes tradiciones"""
    # Diferentes tradiciones de apellidos
    styles = [
        # Estilo español/latinoamericano (dos apellidos)
        lambda: f"{fake.last_name()} {fake.last_name()}",
        # Apellido simple
        lambda: fake.last_name(),
        # Apellido compuesto con guión (estilo anglosajón)
        lambda: f"{fake.last_name()}-{fake.last_name()}",
        # Apellido con partícula (von, de, van, etc.)
        lambda: f"{random.choice(['de', 'van', 'von', 'di', 'del', 'de la', 'dos'])} {fake.last_name()}"
    ]
    
    weights = [0.4, 0.3, 0.2, 0.1]  # Probabilidades para cada estilo
    return random.choices(styles, weights=weights, k=1)[0]()

def generate_user_records(n=1000):
    records = []
    for _ in range(n):
        name = generate_full_name()
        surname = generate_full_surname()
        lang = random.choice(languages)
        telephone = fake.msisdn()[0:9]
        
        # Normalizar nombre y apellido para el email (eliminar espacios y caracteres especiales)
        email_name = name.lower().replace(" ", "").replace("-", "")
        email_surname = surname.lower().replace(" ", "").replace("-", "").replace("de la ", "").replace("del ", "").replace("van ", "").replace("von ", "").replace("di ", "").replace("dos ", "")
        
        email = f"{email_name}.{email_surname}@{fake.free_email_domain()}"
        username = f"{email_name}{random.randint(1, 999)}"
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
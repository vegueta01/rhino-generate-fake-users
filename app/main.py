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
    num_names = random.choices([1, 2, 3], weights=[0.6, 0.35, 0.05], k=1)[0]
    names = [fake.first_name() for _ in range(num_names)]
    return " ".join(names)

def generate_full_surname():
    """Genera apellidos compuestos con probabilidad según diferentes tradiciones"""
    # Probabilidad para la cantidad de apellidos
    num_surnames = random.choices([1, 2, 3, 4], weights=[0.55, 0.35, 0.08, 0.02], k=1)[0]
    
    # Diferentes tipos de apellidos
    surname_types = [
        # Apellido simple
        lambda: fake.last_name(),
        # Apellido con partícula (von, de, van, etc.)
        lambda: f"{random.choice(['de', 'van', 'von', 'di', 'del', 'de la', 'dos'])} {fake.last_name()}"
    ]
    
    # Generar la cantidad de apellidos determinada
    surnames = []
    for _ in range(num_surnames):
        # 85% apellidos simples, 15% con partícula
        surname_func = random.choices(surname_types, weights=[0.85, 0.15], k=1)[0]
        surnames.append(surname_func())
    
    return " ".join(surnames)

def generate_user_records(n=1000):
    records = []
    for _ in range(n):
        name = generate_full_name()
        surname = generate_full_surname()
        lang = random.choice(languages)
        telephone = fake.msisdn()[0:9]
        
        # Normalizar nombre y apellido para el email (eliminar espacios y caracteres especiales)
        email_name = name.lower().replace(" ", "")
        email_surname = surname.lower().replace(" ", "").replace("de la ", "").replace("del ", "").replace("van ", "").replace("von ", "").replace("di ", "").replace("dos ", "")
        
        # Asegurarse de que el email no sea demasiado largo
        if len(email_name) + len(email_surname) > 20:
            # Si es muy largo, acortar el apellido
            email_surname = email_surname[:10]
        
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
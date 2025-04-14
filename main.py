import random
import json
from typing import Optional
from fastapi import FastAPI, Query
from faker import Faker
import pandas as pd

app = FastAPI()
fake = Faker()

# Ejemplos de idiomas
languages = ['en', 'es', 'fr', 'de', 'it', 'jp', 'kr', 'cn', 'ru', 'pt']

# Generador para el campo custom
def generate_custom_field():
    base_keys = [
        ("nivel", lambda: random.randint(1, 100)),
        ("poder", lambda: random.choice(["fuego", "agua", "trueno", "tierra", None])),
        ("activo", lambda: random.choice([True, False])),
        ("inventario", lambda: random.sample(["espada", "escudo", "poción", "llave", "oro"], k=random.randint(1, 4))),
        ("aliado", lambda: fake.first_name() if random.random() > 0.5 else None),
        ("misiones_completadas", lambda: random.randint(0, 50)),
        ("atributos", lambda: {"fuerza": random.randint(1, 10), "agilidad": round(random.uniform(1.0, 10.0), 2)}),
        ("comentario", lambda: fake.sentence(nb_words=6)),
        ("puntos", lambda: random.choice([None, random.randint(0, 1000)])),
        ("historial", lambda: [{"fecha": fake.date(), "evento": fake.word()} for _ in range(random.randint(1, 3))])
    ]
    keys_to_include = random.sample(base_keys, k=random.randint(2, 6))
    return {key: generator() for key, generator in keys_to_include}

# Generador principal
def generate_user_records(n: int):
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
            "custom": json.dumps(custom, ensure_ascii=False)
        })
    return records

# Endpoint
@app.get("/fake-data")
def get_fake_data(count: Optional[int] = Query(default=1000, ge=1, le=10000)):
    """
    Genera datos falsos con estructura avanzada.
    Puedes pasar el parámetro ?count=1000 para definir cuántos registros retornar.
    """
    users = generate_user_records(count)
    df = pd.DataFrame(users)
    return df.to_dict(orient="records")
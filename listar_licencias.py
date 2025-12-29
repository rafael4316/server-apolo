import os
import requests
from datetime import date, datetime

# ----------------------------------------
# Configuración
# ----------------------------------------
BASE_URL = "https://licencia-autoclave.onrender.com"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

if not ADMIN_TOKEN:
    raise RuntimeError("❌ ADMIN_TOKEN no definido en variables de entorno.")

URL = f"{BASE_URL}/licenses?admin_token={ADMIN_TOKEN}"

# ----------------------------------------
# Solicitud
# ----------------------------------------
response = requests.get(URL, timeout=10)

if response.status_code != 200:
    print(f"❌ Error {response.status_code}: {response.text}")
    exit(1)

licenses = response.json()
today = date.today()

print("\n📋 LISTADO DE LICENCIAS\n")

for lic in licenses:
    username = lic["username"]
    key = lic["license_key"]
    machine = lic["machine_id"]
    exp_str = lic["expiration_date"]

    # Estado activación
    estado_activacion = "🟢 ACTIVA" if machine else "⚪ NO ACTIVADA"

    # Fecha de expiración
    if exp_str:
        exp_date = datetime.fromisoformat(exp_str).date()
        days_left = (exp_date - today).days

        if days_left < 0:
            estado_exp = "🔴 EXPIRADA"
        elif days_left <= 7:
            estado_exp = f"🟡 CADUCA EN {days_left} DÍAS"
        else:
            estado_exp = f"🟢 {days_left} días restantes"
    else:
        estado_exp = "♾️ SIN EXPIRACIÓN"

    print(f"""
Usuario   : {username}
Licencia  : {key}
Estado    : {estado_activacion}
Expira    : {estado_exp}
Máquina   : {machine or '-'}
----------------------------------------
""")

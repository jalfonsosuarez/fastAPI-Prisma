import requests

BASE_URL = "http://localhost:8000"

def print_test(name):
    print(f"\n {name}\n"+ "-" * 50)
    
# 1. Login correcto
print_test("Prueba 1: Login con usuario administrador que existe.")
resp = requests.post(f"{BASE_URL}/auth", data={"username": "admin@mail.com", "password": "A123456b"})
print(resp)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    admin_resp = requests.get(f"{BASE_URL}/users", headers=headers)
    print("Status:", admin_resp.status_code)
    print("respuesta:", admin_resp.json())
else:
    print("Error al recibir el token", resp.text)

print_test("Prueba 2: Login con usuario que no existe.")
resp = requests.post(f"{BASE_URL}/auth", data={"username": "other@mail.com", "password": "A123456b"})
print(resp)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    admin_resp = requests.get(f"{BASE_URL}", headers=headers)
    print("Status:", admin_resp.status_code)
    print("respuesta:", admin_resp.json())
else:
    print("Error al recibir el token", resp.text)
    
print_test("Prueba 3: Login con usuario contraseña erronea.")
resp = requests.post(f"{BASE_URL}/auth", data={"username": "admin@mail.com", "password": "A123456"})
print(resp)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    admin_resp = requests.get(f"{BASE_URL}", headers=headers)
    print("Status:", admin_resp.status_code)
    print("respuesta:", admin_resp.json())
else:
    print("Error al recibir el token", resp.text)
    
print_test("Prueba 5: Login sin datos de acceso.")
resp = requests.post(f"{BASE_URL}/auth")
print(resp)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    admin_resp = requests.get(f"{BASE_URL}", headers=headers)
    print("Status:", admin_resp.status_code)
    print("respuesta:", admin_resp.json())
else:
    print("Error al recibir el token", resp.text)
    
print_test("Prueba 6: Login como usuario no admin.")
resp = requests.post(f"{BASE_URL}/auth", data={"username": "user@mail.com", "password": "A123456b"})
print(resp)
if resp.status_code == 200:
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_resp = requests.get(f"{BASE_URL}/users", headers=headers)
    print("Status:", user_resp.status_code)
    print("respuesta:", user_resp.json())
else:
    print("Error al recibir el token", resp.text)
    

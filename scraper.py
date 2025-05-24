import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import os

EMAIL = "mohamed.aziz.mehri.pro@gmail.com"
PASSWORD = "mehriferrari0727"

app = Flask(__name__)

def get_stock():
    try:
        session = requests.Session()

        login_url = "https://app.shipper.market/api/auth/login"
        login_response = session.post(login_url, json={
            "email": EMAIL,
            "password": PASSWORD
        })

        if login_response.status_code != 200:
            print("❌ Erreur de connexion")
            return None

        print("🔐 Login OK:", login_response.json())

        # Essaie de récupérer un token s’il y en a un
        token = login_response.json().get("accessToken")  # adapte le nom du champ selon la réponse réelle
        if not token:
            print("❌ Token manquant dans la réponse")
            return None

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Suppose qu’il y a une vraie route API ici :
        product_api_url = "https://app.shipper.market/api/products/704b3a71-d020-47ad-a945-fffa62fd083e"
        response = session.get(product_api_url, headers=headers)

        if response.status_code != 200:
            print("❌ Erreur chargement API produit")
            return None

        data = response.json()
        print("📦 Données produit:", data)
        

        # Essaye d'extraire le stock du JSON
        stock = data.get("stock")  # adapte ce champ au nom réel dans la réponse
        print(f"✅ Stock récupéré : {stock}")

        return stock
    
    except Exception as e:
        print("❌ Exception dans get_stock:", e)
        return None

@app.route("/get-stock")
def stock_route():
    stock = get_stock()
    if stock is None:
        return jsonify({"error": "stock indisponible"}), 500
    return jsonify({"stock": stock})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


import requests
from bs4 import BeautifulSoup

EMAIL = "mohamed.aziz.mehri.pro@gmail.com"
PASSWORD = "mehriferrari0727"

def get_stock():
    try:
        session = requests.Session()

        # Connexion API (adaptée selon le fonctionnement du site)
        login_url = "https://app.shipper.market/api/auth/login"
        login_response = session.post(login_url, json={
            "email": EMAIL,
            "password": PASSWORD
        })

        if login_response.status_code != 200:
            print("❌ Erreur de connexion")
            return None

        # Charger la page du produit
        product_page_url = "https://app.shipper.market/products/704b3a71-d020-47ad-a945-fffa62fd083e"
        response = session.get(product_page_url)

        if response.status_code != 200:
            print("❌ Erreur chargement produit")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for el in soup.find_all(class_="text-success"):
            txt = el.get_text(strip=True)
            if txt.isdigit():
                return int(txt)
        return None
    except Exception as e:
        print("❌ Exception dans get_stock:", e)
        return None

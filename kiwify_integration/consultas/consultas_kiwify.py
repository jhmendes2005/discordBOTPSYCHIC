import requests
import json
import time
from datetime import datetime, timedelta

class Consulta():

    def __init__(self):
        with open("./kiwify_integration/configs/security.json") as f:
            self.kiwify_account_id = json.load(f)["account_id"]
        
        auth = TempKiwify()
        try:
            self.authorization = auth.get_authorization()
        except Exception as e:
            print(f"Error while getting authorization: {e}")
            self.authorization = None

    def order(self, order_id):
        try:
            url = f"https://public-api.kiwify.com.br/v1/sales/{order_id}"

            headers = {
                "x-kiwify-account-id": f"{self.kiwify_account_id}",
                "Authorization": f"Bearer {self.authorization}"
            }

            response = requests.request("GET", url, headers=headers)
            json1 = response.json()

            email = json1['customer']['email']
            order_id = json1['id']
            product_id = json1['product']['id']

            try:
                product_info = self.product(product_id)
            except Exception as e:
                print(f"Error fetching product info: {e}")
                product_info = None

            print(f"Product INFOS: {product_info}")

            order_info = f"- Order: {order_id} \n- Email: {email} \n- Product ID: {product_id}"
            return order_info
        except Exception as e:
            print(f"Error while ordering: {e}")
            return None

    def product(self, product_id):
        url = f"https://public-api.kiwify.com.br/v1/products/{product_id}"

        headers = {
            "x-kiwify-account-id": f"{self.kiwify_account_id}",
            "Authorization": f"Bearer {self.authorization}"
        }

        response = requests.request("GET", url, headers=headers)
        return response.text
    
class TempKiwify():
    def __init__(self):
        with open("./kiwify_integration/configs/temp.json") as f:
            configdata = json.load(f)
            authorization = configdata["authorization"]
            valid = configdata["valid"]

        with open("./kiwify_integration/configs/security.json") as f:
            configdata2 = json.load(f)
            client_secret = configdata2["client_secret"]
            client_id = configdata2["client_id"]
            account_id = configdata2["account_id"]
        
        self.client_secret = client_secret
        self.client_id = client_id
        self.account_id = account_id
        self.authorization = authorization
        self.valid = valid

    def get_authorization(self):
        # Obtém a data e hora atuais
        data_atual = datetime.now()

        # Supondo que self.valid contenha a data no formato de string
        data_salva_json = self.valid
        
        # Convertendo a data do JSON para um objeto datetime
        data_json = datetime.strptime(data_salva_json, '%Y-%m-%d %H:%M:%S.%f')
        print(data_json)
        print(data_atual)

        # Verificando se a data atual é maior que a data do JSON
        if data_atual > data_json:
            print("[LOG] - AUTHORIZATION EXPIRED")
            print("[LOG] - GENERATING...")
            new_token = self.generate_authorization()
            print("[LOG] - SUCCESS!!")
            return new_token
        else:
            return self.authorization
        
    def generate_authorization(self):
        url = "https://public-api.kiwify.com.br/v1/oauth/token"
        payload = f"client_secret={self.client_secret}&client_id={self.client_id}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        response = requests.request("POST", url, data=payload, headers=headers)
        response_json = response.json()

        access_token = response_json['access_token']
        self.authorization = access_token

        with open('./kiwify_integration/configs/temp.json', 'r') as file:
            data = json.load(file)

        data['authorization'] = access_token

        nova_data = datetime.now() + timedelta(hours=10)
        data['valid'] = nova_data.strftime('%Y-%m-%d %H:%M:%S.%f')

        with open('./kiwify_integration/configs/temp.json', 'w') as file:
            json.dump(data, file, indent=4)

        return access_token
    
class Orders_extract():

    def __init__(self):
        with open("./kiwify_integration/configs/security.json") as f:
            self.kiwify_account_id = json.load(f)["account_id"]
        
        auth = TempKiwify()
        try:
            self.authorization = auth.get_authorization()
        except Exception as e:
            print(f"Error while getting authorization: {e}")
            self.authorization = None

    def save_data_to_json(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def extract_data_page(self, start_date, end_date, page_number, page_size):
        url = "https://public-api.kiwify.com.br/v1/sales"
        querystring = {
            "start_date": start_date,
            "end_date": end_date,
            "page_size": page_size,
            "page_number": page_number  # Adicionando a paginação
        }

        headers = {
            "x-kiwify-account-id": f"{self.kiwify_account_id}",
            "Authorization": f"Bearer {self.authorization}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            return [entry for entry in data['data'] if entry.get('status') == 'paid']
        else:
            print(f"Erro ao recuperar a página {page_number}: {response.status_code}")
            return []

    def extract_all_data(self, start_date, end_date, page_size):
        all_data = []
        page_number = 1
        while True:
            page_data = self.extract_data_page(start_date, end_date, page_number, page_size)
            if not page_data:  # Se a página estiver vazia, terminar a extração
                break
            all_data.extend(page_data)
            page_number += 1
            time.sleep(1)
        filtered_data = [
            {
                "id": entry.get('id'),
                "product": {
                    "id": entry.get('product', {}).get('id')
                },
                "customer": {
                    "id": entry.get('customer', {}).get('id'),
                    "name": entry.get('customer', {}).get('name'),
                    "email": entry.get('customer', {}).get('email'),
                    "cpf": entry.get('customer', {}).get('cpf'),
                    "mobile": entry.get('customer', {}).get('mobile')
                }
            }
            for entry in all_data
        ]
        return filtered_data
    
    def extract_3days(self):
        try:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  
            end_date = datetime.now().strftime('%Y-%m-%d')
            extracted_data = self.extract_all_data(start_date, end_date, page_size=10)
            self.save_data_to_json(extracted_data, "./database/configs/extracted_data.json")
            return True
        except Exception as e:
            print(f"Erro ao tentar extrair os ultimos 3 dias... {e}")
            return None
        

# Exemplo de utilização:
""" order_extractor = Orders_extract()
start_date = (datetime.now() - timedelta(days=88)).strftime('%Y-%m-%d')  # Data de 30 dias atrás
end_date = datetime.now().strftime('%Y-%m-%d')  # Data atual

extracted_data = order_extractor.extract_all_data(start_date, end_date, page_size=10)

# Salvar os dados extraídos em um arquivo JSON
order_extractor.save_data_to_json(extracted_data, "./database/configs/extracted_data.json") """

order_extractor = Orders_extract()
order_extractor.extract_3days()
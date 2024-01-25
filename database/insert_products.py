import json
import mysql.connector

class BancoDeDados:
    def __init__(self):
        with open("./database/configs/config.json") as f:
            config = json.load(f)

        self.conn = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        self.cursor = self.conn.cursor()

    def fechar_conexao(self):
        self.conn.close()

    def inserir_produto(self, produto):
        try:
            query = "INSERT INTO produtos (id, nome, id_role) VALUES (%s, %s, %s)"
            values = (produto['id'], produto['name'], produto['id_role'])
            self.cursor.execute(query, values)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro na inserção do produto {produto['id']}: {err}")

def main():
    banco = BancoDeDados()

    # Carregar produtos do arquivo JSON
    with open("./database/configs/products.json") as json_file:
        produtos_json = json.load(json_file)

        # Inserir cada produto na tabela produtos
        for produto in produtos_json["products"]:
            banco.inserir_produto(produto)

    banco.fechar_conexao()
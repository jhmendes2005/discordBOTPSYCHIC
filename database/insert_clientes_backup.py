import json
import mysql.connector

class BancoDados:
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

    def inserir_cliente_e_compra(self, cliente, compra):
        try:
            # Inserir cliente
            query_cliente = "INSERT INTO clientes (id, name, email, cpf, mobile) VALUES (%s, %s, %s, %s, %s)"
            values_cliente = (cliente['id'], cliente['name'], cliente['email'], cliente['cpf'], cliente['mobile'])
            self.cursor.execute(query_cliente, values_cliente)

            # Inserir compra
            query_compra = "INSERT INTO compras (id, customer_id, product_id) VALUES (%s, %s, %s)"
            values_compra = (compra['id'], cliente['id'], compra['product']['id'])
            self.cursor.execute(query_compra, values_compra)

            self.conn.commit()
            print("Cliente inserido no banco de dados com sucesso:")
            print(cliente)

        except mysql.connector.Error as err:
            print(f"Erro na inserção de cliente e compra: {err}")
            try:
                # Inserir compra
                query_compra = "INSERT INTO compras (id, customer_id, product_id) VALUES (%s, %s, %s)"
                values_compra = (compra['id'], cliente['id'], compra['product']['id'])
                self.cursor.execute(query_compra, values_compra)
                self.conn.commit()
                print("Compra inserida no banco de dados com sucesso:")
                print(compra)

            except mysql.connector.Error as err:
                print(f"Erro na inserção de cliente e compra: {err}")

    def insert_all_data(self):
        # Carregar dados do arquivo JSON
        with open("./database/configs/extracted_data.json") as json_file:
            dados_json = json.load(json_file)
            # Inserir cada cliente e compra nas tabelas
            for dado in dados_json:
                print(dado)
                cliente = dado['customer']
                compra = dado

                self.inserir_cliente_e_compra(cliente, compra)
        self.fechar_conexao()

    def quantidade_clientes(self):
        try:
            query = "SELECT COUNT(*) FROM clientes"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result[0]  # Retorna o número de clientes

        except mysql.connector.Error as err:
            print(f"Erro ao obter a quantidade de clientes: {err}")
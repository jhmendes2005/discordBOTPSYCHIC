import json
import mysql.connector

from database.insert_clientes_backup import BancoDados
from kiwify_integration.consultas import *

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

    def inserir_cliente(self, cliente):
        query = "INSERT INTO clientes (id, name, email, cpf, mobile) VALUES (%s, %s, %s, %s, %s)"
        values = (cliente['id'], cliente['name'], cliente['email'], cliente['cpf'], cliente['mobile'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def inserir_compra(self, compra):
        query = "INSERT INTO compras (id, customer_id, product_id) VALUES (%s, %s, %s)"
        values = (compra['id'], compra['customer_id'], compra['product_id'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def consultar_cliente(self, valor, tipo_consulta='id'):
        if tipo_consulta not in ['id', 'email', 'cpf']:
            raise ValueError("Tipo de consulta inválido. Use 'id', 'email' ou 'cpf'.")

        if tipo_consulta == 'id':
            query = "SELECT * FROM clientes WHERE id = %s"
        elif tipo_consulta == 'email':
            query = "SELECT * FROM clientes WHERE email = %s"
        elif tipo_consulta == 'cpf':
            query = "SELECT * FROM clientes WHERE cpf = %s"

        values = (valor,)

        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error during consultar_cliente: {e}")
            # print("Iniciando extração dos ultimos 15 dias...")
            return None
            """ try:
                if Orders_extract.extract_3days() == True:
                    insert_a = BancoDados
                    insert_a.inserir_cliente_e_compra()
                    try:
                        self.cursor.execute(query, values)
                        return self.cursor.fetchone()
                    except Exception as e:
                        print(f"Error during consultar_cliente: {e}")
                        print("Busca dos ultimos 3 dias falhou...")
            except:
                return None """
            

    def consultar_compra(self, compra_id):
        query = """
            SELECT
                compras.id AS compra_id,
                clientes.id AS cliente_id,
                clientes.name AS cliente_name,
                clientes.email AS cliente_email,
                clientes.cpf AS cliente_cpf,
                clientes.mobile AS cliente_mobile,
                produtos.id AS produto_id
            FROM compras
            JOIN clientes ON compras.customer_id = clientes.id
            JOIN produtos ON compras.product_id = produtos.id
            WHERE compras.id = %s
        """
        values = (compra_id,)

        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error during consultar_compra: {e}")
            return None
        

    def consultar_compras_cliente(self, customer_id):
        query = """
            SELECT
                c.id AS compra_id,
                c.customer_id,
                c.product_id
            FROM compras c
            WHERE c.customer_id = %s
        """
        values = (customer_id,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def listar_produtos_por_nome(self):
        query = "SELECT * FROM produtos ORDER BY nome"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def consultar_produto_por_id(self, produto_id):
        query = "SELECT * FROM produtos WHERE id = %s"
        values = (produto_id,)

        try:
            self.cursor.execute(query, values)
            infos = self.cursor.fetchone()
            name = infos[1]
            role_id = int(infos[2])
            return role_id
        except Exception as e:
            print(f"Error during consultar_produto_por_id: {e}")
            return None
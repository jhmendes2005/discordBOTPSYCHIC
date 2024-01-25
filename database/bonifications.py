import json
import mysql.connector

class BonificationsPoints:
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

    def registrar_usuario(self, user_id):
        # Verificar se o usuário já está registrado
        query = "INSERT IGNORE INTO bonifications_points (user_id, points) VALUES (%s, 0)"
        values = (user_id,)
        self.cursor.execute(query, values)
        self.conn.commit()

    def inserir_pontos(self, user_id, points):
        # Garantir que o usuário esteja registrado antes de inserir pontos
        self.registrar_usuario(user_id)

        # Inserir ou atualizar pontos
        query = "UPDATE bonifications_points SET points = points + %s WHERE user_id = %s"
        values = (points, user_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def consultar_pontos(self, user_id):
        # Garantir que o usuário esteja registrado antes de consultar pontos
        self.registrar_usuario(user_id)

        # Consultar pontos
        query = "SELECT points FROM bonifications_points WHERE user_id = %s"
        values = (user_id,)
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def remover_pontos(self, user_id, points):
        # Garantir que o usuário esteja registrado antes de remover pontos
        self.registrar_usuario(user_id)

        # Remover pontos
        query = "UPDATE bonifications_points SET points = GREATEST(0, points - %s) WHERE user_id = %s"
        values = (points, user_id)
        self.cursor.execute(query, values)
        self.conn.commit()

    def resetar_pontos_todos(self):
        query = "UPDATE bonifications_points SET points = 0"
        self.cursor.execute(query)
        self.conn.commit()

    def obter_top_usuarios(self, quantidade):
        query = "SELECT user_id, points FROM bonifications_points ORDER BY points DESC LIMIT %s"
        values = (quantidade,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
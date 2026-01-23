import mysql.connector
from hashlib import sha256

conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="email_market"
        )
cursor = conexao.cursor()

comando = ""
cursor.execute(comando)
usuarios = cursor.fetchall()

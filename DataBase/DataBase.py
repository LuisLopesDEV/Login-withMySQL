import mysql.connector
import main

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="email_market"
)
cursor = conexao.cursor()
comando = 'INSERT INTO email_market VALUES (default, main.usuario_email, main.usuario_senha)'
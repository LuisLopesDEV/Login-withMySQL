from fasthtml.common import *
import mysql.connector
from hashlib import sha256


def gerar_formulario():
    formulario = Form(
        Input( type='email', cls= 'email', name='email', placeholder='Informe seu email'),
        Input(type='password',cls= 'password',name='password',placeholder='Informe sua senha'),
        Button('Login',cls='envia',),
        method='post',
        action="/login",
        cls='form-login'
    )
    return formulario

usuarios = {}  # dicionário {email: senha}


def salvar_usuario(email, senha):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="email_market"
        )
        hashed_senha = sha256(senha.encode()).hexdigest()
        cursor = conexao.cursor()
        comando = "INSERT INTO cadastro (Email, Senha) VALUES (%s, %s)"
        cursor.execute(comando, (email, hashed_senha))
        conexao.commit()
        print("Usuário salvo com sucesso!")

    except mysql.connector.Error as err:
        print("Erro MySQL:", err)  # Mostra a mensagem exata do MySQL

    finally:
            cursor.close()
            conexao.close()

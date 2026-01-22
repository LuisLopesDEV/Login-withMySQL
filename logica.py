from fasthtml.common import *
import mysql.connector


def gerar_formulario():
    formulario = Form(
        Input( type='email', cls= 'email', name='email', placeholder='Informe seu email'),
        Input(type='password',cls= 'password',name='password',placeholder='Informe sua senha'),
        Button('Login',cls='envia',),
        method='post',
        action="/login",
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

        cursor = conexao.cursor()
        comando = "INSERT INTO cadastro (Email, Senha) VALUES (%s, %s)"
        cursor.execute(comando, (email, senha))
        conexao.commit()
        print("Usuário salvo com sucesso!")

    except mysql.connector.Error as err:
        print("Erro MySQL:", err)  # Mostra a mensagem exata do MySQL

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()

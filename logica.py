from fasthtml.common import *
import mysql.connector
from hashlib import sha256





def gerar_formulario_sign():
    formulario_sign = Form(
        H1('Faça seu Cadastro', cls='titulo_form_sign'),
        Input(type='text', cls='fname', name='fname', placeholder='Insira seu primeiro nome'),
        Input(type='text', cls='lname', name='lname', placeholder='Insira seu ultimo nome'),
        Input(type='date', cls='niver', name='niver', placeholder='Data de nascimento'),
        Input( type='email', cls= 'email', name='email', placeholder='Informe seu email'),
        Input(type='password',cls= 'password',name='password',placeholder='Informe sua senha'),
        Button('Login',cls='envia',),
        method='post',
        action="/sign",
        cls='form-sign'
    )
    return formulario_sign

def gerar_formulario_login():
    formulario_login = Form(
        H1('Faça seu Login', cls='titulo_form_login'),
        Input( type='email', cls= 'email', name='email', placeholder='Informe seu email'),
        Input(type='password',cls= 'password',name='password',placeholder='Informe sua senha'),
        Button('Login',cls='envia',),
        method='post',
        action="/login",
        cls='form-login')
    return formulario_login

usuarios = {}  # dicionário {email: senha}


def salvar_usuario(fname, lname, niver, email, senha):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="email_market"
        )
        hashed_senha = sha256(senha.encode()).hexdigest()

        cursor = conexao.cursor()

        comando = "INSERT INTO cadastro (Primeiro_nome, Ultimo_nome, Nascimento, Email, Senha) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(comando, (fname, lname, niver, email, hashed_senha))
        conexao.commit()


    except mysql.connector.Error as err:
        print("Erro MySQL:", err)  # Mostra a mensagem exata do MySQL

    finally:
            cursor.close()
            conexao.close()

def conferir_login(email, senha):
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="email_market"
        )
        cursor = conexao.cursor()

        comando = "SELECT Email, Senha FROM cadastro"
        cursor.execute(comando)
        usuarios = cursor.fetchall()
        hashed_senha = sha256(senha.encode()).hexdigest()

        for emails, senhas in usuarios:  # Desempacotamento automático
            if emails == email and senhas == hashed_senha:
                return True



    except mysql.connector.Error as err:
        print("Erro MySQL:", err)

    finally:
        cursor.close()
        conexao.close()

from fasthtml.common import *
import mysql.connector
from hashlib import sha256
from secrets import token_urlsafe
from datetime import datetime, timedelta, timezone

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="email_market"
    )


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
        Label(Input('Remember me', type='checkbox', cls='relembrar', name='relembrar', role='switch'), cls='remember'),
        Label(Input('*Aceito os termos e condições', type='checkbox', cls='checkbox', name='checkbox'), cls='remember'),
        Button('Login',cls='envia',),
        method='post',
        action="/login",
        cls='form-login')
    return formulario_login

usuarios = {}


def salvar_usuario(fname, lname, niver, email, senha):
    try:
        db = get_db()
        cursor = db.cursor()

        hashed_senha = sha256(senha.encode()).hexdigest()

        comando = "INSERT INTO cadastro (Primeiro_nome, Ultimo_nome, Nascimento, Email, Senha) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(comando, (fname, lname, niver, email, hashed_senha))
        db.commit()


    except mysql.connector.Error as err:
        print("Erro MySQL:", err)  # Mostra a mensagem exata do MySQL

    finally:
            cursor.close()
            db.close()

def conferir_login(email, senha):
        hashed_senha = sha256(senha.encode()).hexdigest()

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT id_cadastro FROM cadastro WHERE Email=%s AND Senha=%s", (email, hashed_senha))
        usuarios = cursor.fetchone()

        cursor.close()
        db.close()

        return usuarios['id_cadastro'] if usuarios else None

def criar_sessao(usuarios_id, lembrar):
    token = token_urlsafe(32)

    if lembrar:
        expires = datetime.now(timezone.utc) + timedelta(days=30)
    else:
        expires = datetime.now(timezone.utc) + timedelta(hours=0.001)

    db = get_db()
    cursor = db.cursor()

    cursor.execute('INSERT INTO sessions VALUES (%s, %s, %s)', (token, usuarios_id, expires))

    db.commit()
    cursor.close()
    db.close()

    return token, expires

def get_user(request):
    token = request.cookies.get('auth_token')
    if not token:
        return None
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT c.*
        FROM sessions s
        JOIN cadastro c ON c.id_cadastro = s.user_id
        WHERE s.token=%s AND s.expires_at > NOW()
        """, (token,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user
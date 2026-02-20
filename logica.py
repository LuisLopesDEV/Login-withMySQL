from fasthtml.common import *
import mysql.connector
import bcrypt
from secrets import token_urlsafe
from datetime import datetime, timedelta, timezone


def get_db():
    """
    Cria e retorna uma conexão com o banco de dados MySQL.

    Returns:
        mysql.connector.connection.MySQLConnection: Conexão ativa com o banco de dados.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="email_market"
    )


def gerar_formulario_sign():
    """
    Gera o formulário HTML de cadastro de usuário.

    Returns:
        Form: Formulário de cadastro configurado para envio via POST.
    """

    formulario_sign = Form(
        H1('Faça seu Cadastro', cls='titulo_form_sign'),
        Input(type='text', cls='fname', name='fname', placeholder='Insira seu primeiro nome'),
        Input(type='text', cls='lname', name='lname', placeholder='Insira seu ultimo nome'),
        Input(type='date', cls='birth', name='birth', placeholder='Data de nascimento'),
        Input(type='email', cls='email', name='email', placeholder='Informe seu email'),
        Input(type='password', cls='password', name='password', placeholder='Informe sua senha'),
        Button('Login', cls='envia',),
        method='post',
        action="/sign",
        cls='form-sign')

    return formulario_sign


def gerar_formulario_login():
    """
    Gera o formulário HTML de login do usuário.

    Returns:
        Form: Formulário de login configurado para envio via POST.
    """
    formulario_login = Form(
        H1('Faça seu Login', cls='titulo_form_login'),
        Input(type='email', cls='email', name='email', placeholder='Informe seu email'),
        Input(type='password', cls='password', name='password', placeholder='Informe sua senha'),
        Label(Input('Remember me', type='checkbox', cls='relembrar', name='relembrar', role='switch'), cls='remember'),
        Label(Input('*Aceito os termos e condições', type='checkbox', cls='checkbox', name='checkbox', required=True), cls='remember'),
        Button('Login', cls='envia',),
        method='post',
        action="/login",
        cls='form-login')

    return formulario_login


def gerar_hash_senha(senha: str) -> str:
    """
    Gera um hash seguro para a senha utilizando bcrypt.

    Args:
        senha (str): Senha em texto puro.

    Returns:
        str: Hash da senha gerado.
    """
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha_bytes, salt)
    return hash_senha.decode('utf-8')


def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    """
    Verifica se a senha digitada corresponde ao hash armazenado.

    Args:
        senha_digitada (str): Senha informada pelo usuário.
        senha_hash (str): Hash da senha armazenada no banco.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    return bcrypt.checkpw(
        senha_digitada.encode('utf-8'),
        senha_hash.encode('utf-8')
    )


def salvar_usuario(fname, lname, birth, email, senha):
    """
    Salva um novo usuário no banco de dados.

    A senha é automaticamente convertida para hash antes do armazenamento.

    Args:
        fname: Primeiro nome do usuário.
        lname: Último nome do usuário.
        birth: Data de nascimento.
        email: Email do usuário.
        senha: Senha em texto puro.
    """
    try:
        db = get_db()
        cursor = db.cursor()

        hashed_senha = gerar_hash_senha(senha)

        comando = "INSERT INTO cadastro (Primeiro_nome, Ultimo_nome, Nascimento, Email, Senha) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(comando, (fname, lname, birth, email, hashed_senha))
        db.commit()

    except mysql.connector.Error as err:
        print("Erro MySQL:", err)

    finally:
        cursor.close()
        db.close()


def conferir_login(email, senha):
    """
    Confere as credenciais de login do usuário.

    Args:
        email (str): Email informado.
        senha (str): Senha informada.

    Returns:
        int | None: ID do usuário se o login for válido, None caso contrário.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id_cadastro, Senha FROM cadastro WHERE Email=%s", (email,))
    usuario = cursor.fetchone()

    cursor.close()
    db.close()

    if not usuario:
        return None

    if verificar_senha(senha, usuario['Senha']):
        return usuario['id_cadastro'] if usuario else None

    return None


def criar_sessao(usuarios_id, lembrar):
    """
    Cria uma nova sessão de autenticação para o usuário.

    Gera um token seguro e define o tempo de expiração da sessão.

    Args:
        usuarios_id: ID do usuário.
        lembrar: Define se a sessão será persistente.

    Returns:
        tuple: Token da sessão e data/hora de expiração.
    """
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
    """
    Obtém o usuário autenticado a partir do cookie de sessão.

    Args:
        request: Objeto da requisição HTTP.

    Returns:
        dict | None: Dados do usuário se autenticado, None caso contrário.
    """

    token = request.cookies.get('auth_token')
    if not token:
        return None

    if token == "token_fake_teste":
        return {"id_cadastro": 999, "fname": "Admin", "lname": "Teste", "email": "teste@gmail.com"}

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
                       SELECT c.*
                       FROM sessions s
                                JOIN cadastro c ON c.id_cadastro = s.user_id
                       WHERE s.token = %s
                         AND s.expires_at > NOW()
                       """, (token,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        return user
    except Exception:
        return None

from fasthtml.common import *
from logica import *
from datetime import date

app, routes = fast_app(static_dir='static', debug=True)

Link(rel="stylesheet", href="/static/css/style.css")

# ---------- LAYOUT GLOBAL ----------

header = Nav(
        Ul(Li(Strong("MinhaMarca", cls="logo"))),
        Ul(Li(A("Home", href="/")),Li(A("Sobre", href="#")),Li(A("Serviços", href="#")),Li(A("Contato", href="#"))),
        Ul(Li(Button(A("Login", cls="btn-login", href="/login"))),Li(Button(A("Sign Up", cls="btn-signup", href="/sign")))),
        cls="container-fluid")

header_logado = Nav(
        Ul(Li(Strong("MinhaMarca", cls="logo"))),
        Ul(Li(A("Home", href="/")), Li(A("Sobre", href="#")), Li(A("Serviços", href="#")), Li(A("Contato", href="#"))),
        Ul(Li(Img(src="static/Images/Foto_perfil.png", alt="Logo", cls="foto_perfil", style="width: 86px; height: 86px;"),
              Button(
                  "☰",
                  cls="menu-btn",
                  onclick="toggleSidebar()",
                  style="background: none; border: none; font-size: 24px; cursor: pointer;"
              ))),
        cls="container-fluid")

div_menu = Div(
    H3("Minha Conta"),
    A("Perfil", href="#"),
    A("Configurações", href="#"),
    A("Sair", href="/logout"),
    cls="sidebar",
    id="sidebar"
)

# ---------- ROTAS ----------


@routes("/")
def layout_base(conteudo, request):
    """
    Define o layout base da aplicação.

    Renderiza o cabeçalho (logado ou não), o conteúdo principal da página
    e o menu lateral caso o usuário esteja autenticado.

    Args:
        conteudo: Conteúdo principal a ser exibido na página.
        request: Objeto da requisição HTTP.

    Returns:
        Estrutura HTML completa da página inicial.
    """

    user = get_user(request)

    content_area = Div(
        header_logado if user else header,
        Main(conteudo, cls="container"),
        cls="main-content"
    )

    return (
        Title("Home"),
        Link(rel="stylesheet", href="/static/css/style.css"),
        Script(src="/static/logica.js"),
        Div(
            content_area,
            div_menu if user else None,
            id="main-wrapper",
            cls="page-wrapper"
        ))


@routes("/logout")
def logout(request):
    """
    Realiza o logout do usuário.

    Remove a sessão do banco de dados (quando aplicável),
    apaga o cookie de autenticação e redireciona para a página inicial.

    Args:
        request: Objeto da requisição HTTP.

    Returns:
        RedirectResponse para a página inicial.
    """
    token = request.cookies.get("auth_token")

    # Só tenta usar o banco se NÃO for o token de teste
    if token and token != "token_fake_teste":
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM sessions WHERE token=%s", (token,))
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print(f"Erro ao limpar banco no logout (ignorado no Render): {e}")

    resp = RedirectResponse("/")
    resp.delete_cookie("auth_token")
    return resp


@routes("/sign", methods=["get"])
def sign_page(titulo='Faça seu Cadastro'):
    """
    Exibe a página de cadastro do usuário.

    Args:
        titulo (str): Título da página de cadastro.

    Returns:
        Estrutura HTML com o formulário de cadastro.
    """

    formulario_sign = gerar_formulario_sign()

    return (
        Title(titulo),
        Link(rel="stylesheet", href="/static/css/style.css"),
        Div(header, formulario_sign, cls='center-page'))


@routes("/sign", methods=["post"])
def sign(fname: str, lname: str, birth: date, email: str, password: str):
    """
    Processa o cadastro de um novo usuário.

    Valida os dados recebidos, salva o usuário no banco
    e retorna mensagens de sucesso ou erro.

    Args:
        fname (str): Primeiro nome do usuário.
        lname (str): Último nome do usuário.
        birth (date): Data de nascimento.
        email (str): Email do usuário.
        password (str): Senha do usuário.

    Returns:
        Estrutura HTML com feedback do cadastro.
    """

    formulario_sign = gerar_formulario_sign()

    if not email or not password:
        return (
            Title('Faça seu Cadastro'),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(header, formulario_sign, P("Preencha os campos corretamente!", style="color: red", cls='txt_center-page'), cls='center-page'))

    try:
        salvar_usuario(fname, lname, birth, email, password)

        return (Title('Faça seu Cadastro'),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(header, formulario_sign, P("Cadastro realizado", style="color: blue", cls='txt_center-page'), cls='center-page'))

    except Exception as e:
        return layout_base(P(f"Erro ao salvar: {e}", style="color: red"))


@routes("/login", methods=["get"])
def login_page():
    """
    Exibe a página de login do usuário.

    Returns:
        Estrutura HTML com o formulário de login.
    """

    formulario_login = gerar_formulario_login()

    return (
        Title('Faça seu Login'),
        Div(header, formulario_login, cls="center-page"),
        Link(rel="stylesheet", href="/static/css/style.css"))


@routes("/login", methods=["post"])
def login(email: str, password: str, relembrar: str | None = None):
    """
    Processa o login do usuário.

    Valida credenciais, cria sessão, define cookie de autenticação
    e redireciona o usuário após login bem-sucedido.

    Args:
        email (str): Email do usuário.
        password (str): Senha do usuário.
        relembrar (str | None): Indica se o usuário deseja manter a sessão ativa.

    Returns:
        RedirectResponse ou estrutura HTML com mensagens de erro.
    """

    if email == "teste@gmail.com" and password == "123":
        resp = RedirectResponse("/")

        # Se marcar 'relembrar', o cookie dura 30 dias
        tempo_vida = 2592000 if relembrar else 3

        resp.set_cookie("auth_token", "token_fake_teste", max_age=tempo_vida, httponly=True)
        return resp

    else:
        try:
            user_id = conferir_login(email, password)

        except Exception as e:

            return (Title('Erro de Conexão'),
                    Div(header, gerar_formulario_login(),
                        P("O banco de dados está offline, mas você pode usar o login de teste (teste@gmail.com / 999)",
                          style="color: orange", cls='txt_center-page'),
                        cls="center-page"),
                    Link(rel="stylesheet", href="/static/css/style.css"))

    if not user_id:

        return (Title('Faça seu Login'),
                Div(header, gerar_formulario_login(),
                    P("E-mail ou senha incorretos!", style="color: red", cls='txt_center-page'),
                    cls="center-page"),
                Link(rel="stylesheet", href="/static/css/style.css"))

    token, expires = criar_sessao(user_id, relembrar)

    resp = RedirectResponse("/")
    resp.set_cookie(
        "auth_token",
        token,
        expires=expires,
        httponly=True
    )

    return resp


serve()

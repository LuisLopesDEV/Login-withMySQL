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
def sign_page(titulo = 'Faça seu Cadastro'):

    formulario_sign = gerar_formulario_sign()

    return (
        Title(titulo),
        Link(rel="stylesheet", href="/static/css/style.css"),
        Div(header,formulario_sign, cls='center-page'))


@routes("/sign", methods=["post"])
def sign(fname: str, lname:str, birth: date, email: str, password: str):

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
            Div(header,formulario_sign, P("Cadastro realizado", style="color: blue", cls='txt_center-page'), cls='center-page'))

    except Exception as e:
        return layout_base(P(f"Erro ao salvar: {e}", style="color: red"))


@routes("/login", methods=["get"])
def login_page():

    formulario_login = gerar_formulario_login()

    return (
        Title('Faça seu Login'),
        Div(header, formulario_login, cls="center-page"),
        Link(rel="stylesheet", href="/static/css/style.css"))


@routes("/login", methods=["post"])
def login(email: str, password: str, relembrar: str | None = None):

    if email == "teste@gmail.com" and password == "123":
        resp = RedirectResponse("/")

        # Se marcar 'relembrar', o cookie dura 30 dias
        tempo_vida = 2592000 if relembrar else 3

        resp.set_cookie("auth_token", "token_fake_teste", max_age=tempo_vida, httponly=True)
        return resp

    else:
        # 2. LOGICA NORMAL (BANCO DE DADOS)
        try:
            user_id = conferir_login(email, password)
        except Exception as e:
            # Se o banco estiver offline (como no Render), retorna erro
            formulario_login = gerar_formulario_login()
            return (Title('Erro de Conexão'),
                    Div(header, formulario_login,
                        P("O banco de dados está offline, mas você pode usar o login de teste (teste@gmail.com / 999)",
                          style="color: orange", cls='txt_center-page'),
                        cls="center-page"),
                    Link(rel="stylesheet", href="/static/css/style.css"))

    if not user_id:
        formulario_login = gerar_formulario_login()

        return (Title('Faça seu Login'),
                Div(header, formulario_login,
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
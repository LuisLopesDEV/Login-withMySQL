from fasthtml.common import *
from logica import *
from datetime import date

app, routes = fast_app(static_dir='static', debug=True)

Link(rel="stylesheet", href="/static/css/style.css")
# ---------- LAYOUT GLOBAL (PRIMEIRO) ----------

header = Nav(
    Ul(Li(Strong("MinhaMarca", cls="logo"))),
    Ul(Li(A("Home", href="/")), Li(A("Sobre", href="#"))),
    Ul(Li(Button(A("Login", href="/login")))),
    cls="container-fluid"
)

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
            content_area,  # Agora o conteúdo e o header estão juntos
            div_menu if user else None,
            id="main-wrapper",
            cls="page-wrapper"
        ))


@routes("/logout")
def logout(request):
    token = request.cookies.get("auth_token")

    if token:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM sessions WHERE token=%s", (token,))
        db.commit()
        cursor.close()
        db.close()

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
def sign(fname: str, lname:str, niver: date,email: str, password: str):
    formulario_sign = gerar_formulario_sign()

    if not email or not password:
        return (
            Title('Faça seu Cadastro'),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(header, formulario_sign, P("Preencha os campos corretamente!", style="color: red", cls='txt_center-page'), cls='center-page'))

    try:

        salvar_usuario(fname, lname, niver, email, password)

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
def login(email:str, password:str, relembrar: str | None = None):
    formulario_login = gerar_formulario_login()

    user_id = conferir_login(email, password)

    if not user_id:
        return (Title('Faça seu Login'),
                      Div(header, formulario_login,
                          P("Preencha os campos corretamente!", style="color: red", cls='txt_center-page'),
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
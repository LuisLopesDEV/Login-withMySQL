from fasthtml.common import *
from logica import gerar_formulario_login ,gerar_formulario_sign, salvar_usuario, conferir_login
from datetime import date
app, routes = fast_app(static_dir='static', debug=True)
from time import sleep

@routes("/", methods=["get"])
def layout_base(conteudo, titulo="Home"):

    return (
        Title(titulo),
        Link(rel="stylesheet", href="/static/css/style.css"),
        Div(header,Main(conteudo, cls="container"), cls="page-wrapper"))


@routes("/sign", methods=["get"])
def sign_page(titulo = 'Faça seu Cadastro'):
    formulario_sign = gerar_formulario_sign()
    return (Title(titulo),
        Link(rel="stylesheet", href="/static/css/style.css"),
        Div(header,formulario_sign, cls='center-page')
    )


@routes("/sign", methods=["post"])
def sign(fname: str, lname:str, niver: date,email: str, password: str):
    formulario_sign = gerar_formulario_sign()

    if not email or not password:
        return (Title('Faça seu Cadastro'),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(header, formulario_sign, P("Preencha os campos corretamente!", style="color: red", cls='txt_center-page'), cls='center-page')
        )
    try:
        salvar_usuario(fname, lname, niver, email, password)

        return (Title('Faça seu Cadastro'),
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(header,formulario_sign, P("Cadastro realizado", style="color: blue", cls='txt_center-page'), cls='center-page')
        )
    except Exception as e:
        return layout_base(P(f"Erro ao salvar: {e}", style="color: red"))


@routes("/login", methods=["get"])
def login_page():

    formulario_login = gerar_formulario_login()

    return (Title('Faça seu Login'),
                  Div(header, formulario_login, cls="center-page"),
                  Link(rel="stylesheet", href="/static/css/style.css"))


@routes("/login", methods=["post"])
def login(email:str, password:str):
    formulario_login = gerar_formulario_login()

    if not email or not password:
        return (Title('Faça seu Login'),
                      Div(header, formulario_login,
                          P("Preencha os campos corretamente!", style="color: red", cls='txt_center-page'),
                          cls="center-page"),
                      Link(rel="stylesheet", href="/static/css/style.css"))
    try:
        resultado = conferir_login(email, password)
        if resultado:
            return (Title('Faça seu Login'),
                          Meta(http_equiv="refresh", content="3; url=/"),
                          Link(rel="stylesheet", href="/static/css/style.css"),
                          Div(header, formulario_login,
                              P("Login realizado com sucesso!", style="color: blue"),
                              P("Aguarde, você será redirecionado em instantes..."),
                              cls="center-page"))
        else:
            return (Title('Faça seu Login'),
                          Div(header, formulario_login, P('Senha incorreta!', cls='txt_center-page'),
                              cls="center-page"),
                          Link(rel="stylesheet", href="/static/css/style.css"))
    except Exception as e:
        return Titled('Faça seu Login',
                      Div(header, formulario_login,
                          P(f'Erro ao salvar {e}', cls='txt_center-page', style="color: red"),
                          cls="center-page"))
serve()

header = Nav(
        Ul(Li(Strong("MinhaMarca", cls="logo"))),
        Ul(Li(A("Home", href="/")),Li(A("Sobre", href="#")),Li(A("Serviços", href="#")),Li(A("Contato", href="#"))),
        Ul(Li(Button(A("Login", cls="btn-login", href="/login"))),Li(Button(A("Sign Up", cls="btn-signup", href="/sign")))),
        cls="container-fluid")
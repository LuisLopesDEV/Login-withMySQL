from fasthtml.common import *
from logica import gerar_formulario, salvar_usuario

app, routes = fast_app(static_dir='static', debug=True)


@routes("/")
def homepage():
    return Titled(
        "Home",
        Link(rel="stylesheet", href="/static/css/style.css"),
        A('Criar Conta', href='/login')
    )

@routes("/login", methods=["get"])
def login_page():
    formulario = gerar_formulario()
    return Titled(
        "Login",
        Link(rel="stylesheet", href="/static/css/style.css"),
        Div(formulario, cls='center-page')
    )

@routes("/login", methods=["post"])
def login(email: str, password: str):
    salvar_usuario(email, password)
    return Titled(
        "Sucesso",
        Link(rel="stylesheet", href="/static/css/style.css"),
        P("Dados salvos no banco com sucesso!")
    )

serve()
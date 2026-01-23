from fasthtml.common import *
from logica import gerar_formulario, salvar_usuario

app, routes = fast_app(static_dir='static', debug=True)

@routes("/", methods=["get"])
def layout_base(conteudo, titulo="Home"):

    header = Nav(
        Ul(Li(Strong("MinhaMarca", cls="logo"))),
        Ul(
            Li(A("Home", href="/")),
            Li(A("Sobre", href="#")),
            Li(A("Serviços", href="#")),
            Li(A("Contato", href="#")),
        ),
        Ul(
            Li(Button(A("Login", cls="btn-login", href="/login"))),
            Li(Button(A("Sign Up", cls="btn-signup", href="/sign"))),
        ),
        cls="container-fluid"
    )

    return (
        Title(titulo),
        Link(rel="stylesheet", href="/static/css/style.css"),
        Div(
            header,
            Main(conteudo, cls="container"),  # Container centraliza o conteúdo
            cls="page-wrapper"
        )
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

    formulario = gerar_formulario()

    if not email or not password:
        return Titled(
            "Login",
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(formulario, P("Preencha os campos corretamente!", style="color: red", cls='txt_center-page'), cls='center-page')
        )
    try:
        salvar_usuario(email, password)

        return Titled(
            "Login",
            Link(rel="stylesheet", href="/static/css/style.css"),
            Div(formulario, P("Login realizado", style="color: blue", cls='txt_center-page'), cls='center-page')
        )
    except Exception as e:
        return layout_base(P(f"Erro ao salvar: {e}", style="color: red"))

serve()
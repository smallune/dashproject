import dash
from dash import html

dash.register_page(__name__, path = "/page2", name = "Health Effects")

layout = html.Div(html.H2("Health Effects", className = "centered-header"))
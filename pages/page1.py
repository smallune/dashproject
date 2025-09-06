import dash
from dash import html

dash.register_page(__name__, path = "/page1", name = "Sales")

layout = html.Div()
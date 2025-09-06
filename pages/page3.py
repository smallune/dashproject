import dash
from dash import html

dash.register_page(__name__, path = "/page3", name = "Demographics")

layout = html.Div()
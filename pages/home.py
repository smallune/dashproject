import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/")

layout = html.Div([
    html.H2("Caffeine Dashboard", className = "centered-header"),
    html.P("Team 14", className = "centered-header")
])

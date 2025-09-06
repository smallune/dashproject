import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/")

layout = html.Div([
    html.H2("Energy Drinks Dashboard", className = "centered-header"),
    html.P("Team 14", className = "centered-header"),
    
    html.Div([
        html.P([
            "This dashboard features a range of data visualizations related to recent consumption and effects of energy drinks in the US.",
            html.Br(),
            "Page 1: Sales data for PepsiCo and Coca-Cola brand energy drinks, visualizing the regional differences in sales trends over the past 5 years.",
            html.Br(),
            "Page 2: Health effects (TODO).",
            html.Br(),
            "Page 3: Demographics (TODO)."
        ], className = "centered-paragraph")
    ])

])

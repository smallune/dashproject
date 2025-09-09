# AI Assistance: ChatGPT helped with how to best use dbc cards in combination with
# links to connect with the website's other pages.

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path = "/")

layout = html.Div([
    
    html.H2("Energy Drink Dashboard", className = "home-header"),
    html.P("Team 14", className = "home-header"),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            dcc.Link(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Sales Data"),
                        html.P("Click to explore sales data of energy drinks within the past 5 years")
                    ]),
                    className = "info-card"
                ),
                href = "/page1",
                style = {"textDecoration": "none"}
            ),
            md = 4
        ),
        dbc.Col(
            dcc.Link(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Regional Popularity"),
                        html.P("Click to compare the differences in brand popularity across the US")
                    ]),
                    className = "info-card"
                ),
                href = "/page3",
                style = {"textDecoration": "none"}
            ),
            md = 4
        ),

        dbc.Col(
            dcc.Link(
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Health Effects"),
                        html.P("Click to see health data related to energy drink consumption")
                    ]),
                    className = "info-card"
                ),
                href = "/page2",
                style = {"textDecoration": "none"}
            ),
            md = 4
        ),
    ], className = "swell"),
], className = "page-padding")
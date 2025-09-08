from dash import html, dcc, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
from dash import html

register_page(__name__, path = '/page4', name = 'About us')

layout = html.Div(
    children = [
        html.H1('About Us', style = {'textAlign': 'center'}),
        html.P('This dashboard was created by Team 14 for the Competing Through BusAnalytics course at William & Mary.'),
        html.P('We hope you find this dashboard informative and engaging!'),
        dbc.Row([  
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="static/images/Small_Conner_H_250818005-2.jpg", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Conner Small", className="card-title"),
                                html.P(
                                    "Some quick example text to build on the card title and "
                                    "make up the bulk of the card's content.",
                                    className="card-text",
                                ),
                                html.A(
                                    html.Button('Contact me', id='email-button', className = 'email-button'),  # The button itself
                                    href='mailto:chsmall@wm.edu',
                                    target='_blank'  # Opens the email client in a new tab/window
                                )
                            ]
                        ),
                    ],
                    className = 'contact-info-card'
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="static/images/Levy_Julia_250818002-2.jpg", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Julia Levy", className="card-title"),
                                html.P(
                                    "Some quick example text to build on the card title and "
                                    "make up the bulk of the card's content.",
                                    className="card-text",
                                ),
                                html.A(
                                    html.Button('Contact me', id='email-button', className = 'email-button'),  # The button itself
                                    href='mailto:jdlevy@wm.edu',
                                    target='_blank'  # Opens the email client in a new tab/window
                                )
                            ]
                        ),
                    ],
                    className = 'contact-info-card'
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardImg(src="static/images/Chirasittikon_Tai_250818005.jpg", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Tai Chirasittikorn ", className="card-title"),
                                html.P(
                                    "Some quick example text to build on the card title and "
                                    "make up the bulk of the card's content.",
                                    className="card-text",
                                ),
                                html.A(
                                    dbc.Button('Contact me', id='email-button', className = 'email-button'),  # The button itself
                                    href='mailto:tchirasittikor01@wm.edu',
                                    target='_blank'  # Opens the email client in a new tab/window
                                )
                            ]
                        ),
                    ],
                    className = 'contact-info-card'
                )
            )
        ])
    ], className = "page-padding"
)
# AI Assistance: ChatGPT helped generate our profile pictures to hold a product of enegy drinks.
# AI Assistance: CoPilot helped with the instructions to make profile cards with email button directly to send email.


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
                        dbc.CardImg(src="static/images/Small_Conner.png", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Conner Small"),
                                html.P(
                                    "\"Just drink water!\"",
                                ),
                                html.A(
                                    html.Button('Contact me', id='email-button', className = 'email-button'),
                                    href = 'mailto:chsmall@wm.edu',
                                    target = '_blank'
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
                        dbc.CardImg(src="static/images/Levy_Julia.png", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Julia Levy"),
                                html.P(
                                    "\"Don't have a 5-Hour Extra Strength in your hand like I do!\"",
                                ),
                                html.A(
                                    html.Button('Contact me', id='email-button', className = 'email-button'),
                                    href = 'mailto:jdlevy@wm.edu',
                                    target = '_blank'
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
                        dbc.CardImg(src="static/images/Chirasittikon_Tai.png", top=True),
                        dbc.CardBody(
                            [
                                html.H4("Tai Chirasittikorn "),
                                html.P(
                                    "Some quick example text to build on the card title and "
                                    "make up the bulk of the card's content.",
                                ),
                                html.A(
                                    dbc.Button('Contact me', id='email-button', className = 'email-button'),
                                    href='mailto:tchirasittikor01@wm.edu',
                                    target='_blank'
                                )
                            ]
                        ),
                    ],
                    className = 'contact-info-card'
                )
            )
        ], className = 'swell'),
    ], className = "page-padding"
)
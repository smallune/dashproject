# AI Assistance: ChatGPT explained how to change the host for deployment on Render.

from dash import Dash, dcc, html
import dash
import dash_bootstrap_components as dbc
import os

# initialize app
app = Dash(__name__, use_pages = True, suppress_callback_exceptions = True,
           external_stylesheets = [dbc.themes.YETI], title = "Energy Drink Trends")

server = app.server # for deployment

app.layout = html.Div([
    dbc.NavbarSimple(
        children = [
            dbc.NavLink("Home", href = "/", active = "exact"),
            dbc.NavLink("Sales", href = "/page1", active = "exact"),
            dbc.NavLink("Demographics", href = "/page3", active = "exact"),
            dbc.NavLink("Health Effects", href = "/page2", active = "exact"),
            dbc.NavLink("About us", href = "/page4", active = "exact")
        ], 
        brand = "Energy Drink Dashboard",
        brand_href = "/"
    ),
    dash.page_container,
    html.Footer([
        html.Div([
            html.Img(src="static/images/product_brand/redbull.webp", className = 'product-image'),
            html.Img(src="static/images/product_brand/monster.webp", className = 'product-image'),
            html.Img(src="static/images/product_brand/bang.webp", className = 'product-image'),
            html.Img(src="static/images/product_brand/celsius.webp", className = 'product-image'),
            html.Img(src="static/images/product_brand/c4.png", className = 'product-image')
        ], className = 'crop-image'),
    ], className = "footer")
], className = "flex-wrapper")

# Render sets $PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host = "0.0.0.0", port = port, debug = False)
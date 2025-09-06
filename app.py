from dash import Dash, dcc, html
import dash
import dash_bootstrap_components as dbc

# initialize app
app = Dash(__name__, use_pages = True, suppress_callback_exceptions = True,
           external_stylesheets = [dbc.themes.YETI], title = "Caffeine Drink Impacts")
server = app.server # for deployment

app.layout = html.Div([
    dbc.NavbarSimple(
        children = [
            dbc.NavLink("Home", href = "/", active = "exact"),
            dbc.NavLink("Sales", href = "/page1", active = "exact"),
            dbc.NavLink("Health Effects", href = "/page2", active = "exact"),
            dbc.NavLink("Demographics", href = "/page3", active = "exact"),
            dbc.NavLink("About us", href = "/page4", active = "exact")
        ], 
        brand = "Drink App"
    ),
    dash.page_container
])

#"Yes"

if __name__ == "__main__":
    app.run(debug = True)
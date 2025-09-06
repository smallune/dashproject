import dash
from dash import html, dcc, Input, Output, callback
import kagglehub
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__, path = "/page1", name = "Sales")

# download latest kaggle dataset for soft drink sales
path = kagglehub.dataset_download("prasadahirekar/soft-drink-sales")

# load data, convert purchase date to pandas datetime format,
# and filter dataset for only energy drinks
df = pd.read_csv(f"{path}/soft_drink_sales.csv")
df["Purchase Date"] = pd.to_datetime(df["Purchase Date"])
df_energydrinks = df[df["Product"] == "Energy Drink"]

states = sorted(df_energydrinks["Customer State"].unique())

layout = html.Div([
    html.H2("Sales Data", className="centered-header"),
    dbc.Row([
        dbc.Col(
            [
                dbc.Alert([
                    html.H4("Select a State", className="alert-heading"),
                    html.P("Use the dropdown below to visualize energy drink units sold over time for a specific state.")
                ], color = "secondary"),
                dcc.Dropdown(
                    id = "state-dropdown",
                    options=[{"label": state, "value": state} for state in states],
                    value=states[0],
                    clearable=False,
                    style={"width": "100%"}
                ),
                dcc.Graph(id="units-sold-graph")
            ]),
        dbc.Col(
            [
                dbc.Alert([
                    html.H4("Google Search Trends", className="alert-heading"),
                    html.P("This section could display Google Trends data for 'energy drink' searches in the selected state or nationwide.")
                ], color="secondary", className="mb-4"),
                # You can add a graph or other content here later
            ])
    ], justify="center", align="start"),
    dbc.Row([
        dbc.Card(
            dbc.CardBody([
                html.P([
                    "Sales data sourced from Kaggle. ",
                    html.A("View Dataset", href="https://www.kaggle.com/datasets/prasadahirekar/soft-drink-sales", target="_blank")
                ])
            ])
        )
    ])
], className = "page-padding")

@callback(
    Output("units-sold-graph", "figure"),
    Input("state-dropdown", "value")
)

def update_graph(state):
    filtered = df_energydrinks[df_energydrinks["Customer State"] == state].copy()
    # Change the line below to adjust bin width:
    filtered["Period"] = filtered["Purchase Date"].dt.to_period("Q").astype(str)  # "W" for week, "M" for month, "Q" for quarter, etc.
    grouped = filtered.groupby("Period", as_index=False)["Units Sold"].sum()
    fig = px.bar(
        grouped,
        x="Period",
        y="Units Sold",
        title=f"Energy Drink Units Sold Per Quarter in {state}"
    )
    fig.update_layout(xaxis_title="Period", yaxis_title="Units Sold")
    return fig


# AI Assistance: used ChatGPT to help brainstorming how to
# best vizualize trends in sales data over time. CoPilot within
# VSCode was used to help write the layout and callback code.
# For vizualization syntax assistance, the CoPilot "tab" auto-complete
# feature was useful. 
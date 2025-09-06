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

brands = sorted(df_energydrinks["Company"].unique())

# sorted list of state names
states = sorted(df_energydrinks["Customer State"].unique())

layout = html.Div([
    
    html.H2("Sales Data", className="centered-header"),
    
    dcc.Dropdown(
        id = "state-dropdown",
        options = [{"label": state, "value": state} for state in states],
        value = states[0],
        clearable = False,
        style = {"width": "50%", "margin": "0 auto", "marginBottom": "20px"}
    ),
    
    dbc.Row([
        
        dbc.Col([
            
            dbc.Alert([
                html.H4("Unit Sales"),
                html.P("Use dropdown to visualize state energy drink sales by quarter."),
            ], color = "secondary"),
            
            html.Div([
                html.Label("Select Brands:"),
                dcc.Checklist(
                    id="company-checklist",
                    options=[{"label": brand, "value": brand} for brand in brands],
                    value=brands,  # All selected by default
                    inline=True,
                    style={"marginBottom": "20px"}
                ),
            ], style={"marginBottom": "20px"}),
                
            dcc.Graph(id = "units-sold-graph"),
                
            dbc.Card(
                dbc.CardBody(html.P([
                    "Sales data sourced from Kaggle. ",
                    html.A("View Dataset", href="https://www.kaggle.com/datasets/prasadahirekar/soft-drink-sales", target="_blank")
                ], style = {"marginBottom": "0px"}))
            )
                
        ], width = 6)
        
    ], justify = "center", align = "start"),
    
], className = "page-padding")

@callback(
    Output("units-sold-graph", "figure"),
    Input("state-dropdown", "value"),
    Input("company-checklist", "value")
)

def update_graphs(state, selected_brands):
    filtered = df_energydrinks[
        (df_energydrinks["Customer State"] == state) &
        (df_energydrinks["Company"].isin(selected_brands))
    ].copy()
    filtered["Period"] = filtered["Purchase Date"].dt.to_period("Q").astype(str)
    grouped = filtered.groupby(["Period", "Company"], as_index=False)["Units Sold"].sum()
    fig_sales = px.bar(
        grouped,
        x="Period",
        y="Units Sold",
        color="Company",
        barmode="group",
        title=f"Energy Drink Units Sold Per Quarter in {state}"
    )
    fig_sales.update_layout(xaxis_title="Period", yaxis_title="Units Sold")
    return fig_sales


# AI Assistance: used ChatGPT to help brainstorming how to
# best vizualize trends in sales data over time. CoPilot within
# VSCode was used to help write the layout and callback code.
# For vizualization syntax assistance, the CoPilot "tab" auto-complete
# feature was useful. 
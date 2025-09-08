# AI Assistance: used ChatGPT to help brainstorm how to
# best vizualize trends in sales data over time. CoPilot within
# VSCode was used to help write the layout and callback code, and helped
# with dataset filtering syntax. For additional layout syntax assistance, 
# the CoPilot "tab" auto-complete feature was useful. All layout and visualization
# elements structured by gen AI were reviewed, understood, and revised to
# better suit our project direction and visual preferences.

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

# sorted list of states for vizualization
states = sorted(df_energydrinks["Customer State"].unique())

layout = dbc.Container([
    
    html.H2("Sales Data", className="centered-header"),
    
    # dbc.Alert("Use dropdown to select state.", 
    #           color = "secondary", 
    #           className = "centered-header", 
    #           style = {"width": "25%", "margin": "0 auto", "marginBottom": "20px"}),
    
    dcc.Dropdown(
        id = "state-dropdown",
        options = [{"label": state, "value": state} for state in states],
        value = "Virginia",
        clearable = False,
        style = {"width": "50%", "margin": "0 auto", "marginBottom": "20px"},
        placeholder = "Select a state"
    ),
    
    dbc.Row([
        
        dbc.Col([
            
            dcc.Graph(id = "units-sold-graph"),
                
            dbc.Card(
                dbc.CardBody(html.P([
                    "Sales data sourced from Kaggle. ",
                    html.A("View Dataset", href = "https://www.kaggle.com/datasets/prasadahirekar/soft-drink-sales", target="_blank")
                ], style = {"textAlign": "center", "margin": "20px", "fontSize": "14px"}))
            )
                
        ], style = {"maxWidth": "800px"})
        
    ], justify = "center", align = "start", className = "swell"),
    
], fluid = True, className = "page-padding")

@callback(
    Output("units-sold-graph", "figure"),
    Input("state-dropdown", "value"),
)

def update_graphs(state):
    
    filtered = df_energydrinks[df_energydrinks["Customer State"] == state].copy()
    filtered["Period"] = filtered["Purchase Date"].dt.to_period("Q").astype(str)
    grouped = filtered.groupby("Period", as_index = False)["Units Sold"].sum()
    
    sales = px.bar(
        grouped,
        x = "Period",
        y = "Units Sold",
        title = f"Energy Drink Units Sold Per Quarter in {state}"
    )
    
    sales.update_layout(xaxis_title = "Period", yaxis_title = "Units Sold", plot_bgcolor = "white")

    return sales
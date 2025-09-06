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


# df2 = pd.read_csv("data/geoMap.csv")
# df_trends = df2
# print(df_trends.head())

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
                
            dcc.Graph(id = "units-sold-graph"),
                
            dbc.Card(
                dbc.CardBody(html.P([
                    "Sales data sourced from Kaggle. ",
                    html.A("View Dataset", href="https://www.kaggle.com/datasets/prasadahirekar/soft-drink-sales", target="_blank")
                ], style = {"marginBottom": "0px"}))
            )
                
        ]),
        
        dbc.Col([
            
                dbc.Alert([
                    html.H4("Google Search Trends"),
                    html.P("Due to the limited quantity of sales data available from the dataset, Google Trends data can provide more insight into the popularity of energy drinks in the US.")
                ], color="secondary"),
                
                # dcc.Graph(id="trends-graph")
       
        ])
        
    ], justify = "center", align = "start"),
    
], className = "page-padding")

@callback(
    Output("units-sold-graph", "figure"),
    # Output("trends-graph", "figure"),
    Input("state-dropdown", "value")
)

def update_graphs(state):
    # Sales bar plot (unchanged)
    filtered = df_energydrinks[df_energydrinks["Customer State"] == state].copy()
    filtered["Period"] = filtered["Purchase Date"].dt.to_period("Q").astype(str)
    grouped = filtered.groupby("Period", as_index=False)["Units Sold"].sum()
    fig_sales = px.bar(
        grouped,
        x="Period",
        y="Units Sold",
        title=f"Energy Drink Units Sold Per Quarter in {state}"
    )
    fig_sales.update_layout(xaxis_title="Period", yaxis_title="Units Sold")

    # Google Trends bar plot (updated column names)
    # popularity_col = [col for col in df_trends.columns if col != "Region"][0]  # Automatically get the popularity column
    # filtered_trends = df_trends[df_trends["Region"] == state]
    # fig_trends = px.bar(
    #     filtered_trends,
    #     x="Region",
    #     y=popularity_col,
    #     title=f"Google Search Popularity for 'Energy Drink' in {state} (last 5 years)"
    # )
    # fig_trends.update_layout(xaxis_title="State", yaxis_title="Popularity")

    return fig_sales#, fig_trends


# AI Assistance: used ChatGPT to help brainstorming how to
# best vizualize trends in sales data over time. CoPilot within
# VSCode was used to help write the layout and callback code.
# For vizualization syntax assistance, the CoPilot "tab" auto-complete
# feature was useful. 
#Importing packages (clean this up)
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import requests
import matplotlib.pyplot as plt
import seaborn as sns 

#Registering the page 
dash.register_page(__name__, path = "/page2", name = "Health Effects")

#ADD COMMENTS AND CHANGE STYLING/FORMATTING 
#Make the reactions only the top 5 most common for each brand 

#Loading in API url  
url = "https://api.fda.gov/food/event.json?search=products.name_brand:%22RED+BULL%22+OR+products.name_brand:%22MONSTER+ENERGY%22+OR+products.name_brand:%225+HOUR%22+OR+products.name_brand:%22BANG%22+OR+products.name_brand:%22C4%22+OR+products.name_brand:%22CELSIUS%22&limit=1000"
r = requests.get(url, timeout = 30)
r.raise_for_status()
results = r.json()["results"]

#Determining what brands, reactions, and outcomes to filter for 
energy_drinks_reactions = {
    "name_brand": ["RED BULL", "MONSTER ENERGY", "CELSIUS", "5 HOUR ENERGY", "C4"],
    "reactions": ["Blood pressure","HEART RATE","Dizziness","ANXIETY","NERVOUSNESS","CHEST", "MYOCARDIAL INFARCTION","PALPITATIONS","DYSPNOEA", "STROKE", "CONVULSIONS","LOSS OF CONSCIOUSNESS"],
    "outcomes": ["Hospitalization","Death","Life Threatening"]
}

#Creating a dataframe that consolidates the information from the API
#take out outcome and date 
records = []
for report in results:
    if "products" in report:
        for product in report["products"]:
            name_brand = product["name_brand"] if "name_brand" in product else ""
            if name_brand in energy_drinks_reactions["name_brand"]:
                if "reactions" in report and report["reactions"]:
                    for reaction in report["reactions"]:
                        records.append({
                            "name_brand": name_brand,
                            "reactions": reaction})

filtered_df = pd.DataFrame(records)
filtered_df["reactions"] = filtered_df["reactions"].str.lower()

#Counting every reaction for each brand (might not need)
brand_reaction_counts = {}
for brand in filtered_df["name_brand"].unique():
    brand_df = filtered_df[filtered_df["name_brand"] == brand]
    reaction_counts = brand_df["reactions"].value_counts().to_dict()
    brand_reaction_counts[brand] = reaction_counts
# print(brand_reaction_counts)

# Counting total reactions for each brand 
total_brand_reactions = {}
for brand in filtered_df["name_brand"].unique():
    total_reactions_per_brand = sum(brand_reaction_counts[brand].values())
    total_brand_reactions[brand] = total_reactions_per_brand

total_reactions_df = pd.Series(total_brand_reactions).reset_index()
total_reactions_df.columns = ["name_brand", "count_of_reactions"]
#print(total_reactions_df)


#Top bar
navbar = html.Div([
   html.H1("Health Effects of Caffeinated Drinks", className = "centered-header") 
])

##Add dropdown that gives most common reaction for each brand 
#Dropdown (left column)
reactions = dbc.Card([
        dbc.CardHeader("Reactions"),
        dbc.CardBody(
            [
                dbc.Label("Select Energy Drink Brand"),
                dcc.Dropdown(
                    id="brand-dropdown",
                    options=[{"label": k, "value": k} for k in brand_reaction_counts.keys()],
                    value="RED BULL",
                    clearable=False,
                ),
                html.Br(),
                html.Div(id ="reaction-display", className= "mt-3"),
                html.Hr(),
                html.Small(
                    "Data source: openfda.gov (no API key required).",
                    className="text-muted",
                ),
            ])
    ],className="mb-5",)

@callback(
    Output("reaction-display", "children"),
    Input("brand-dropdown", "value")
)

def update_reactions(selected_brand):
    if selected_brand in brand_reaction_counts:
        reactions = brand_reaction_counts[selected_brand]
        reaction_list = [
            html.Li(f"{reaction}: {count} reports")
            for reaction, count in reactions.items()
        ]
        return [
            html.H5(f"Reactions for {selected_brand}:"),
            html.Ul(reaction_list, className="list-unstyled")
        ]
    return "No reactions found for this brand."

#Barplot
#March 14 2025 was latest date August 11 2004 (over 20 years)
brand_order = ["5 HOUR ENERGY", "RED BULL", "MONSTER ENERGY", "CELSIUS", "C4"]
def create_figure():
    fig = px.bar(
        total_reactions_df,
        x="count_of_reactions",
        y="name_brand",
        title="Energy Drink Reactions by Brand in the last 20 years",
        color = "name_brand",
        color_discrete_map = {
            "5 HOUR ENERGY": "#7242F7",
            "RED BULL": "#8965EA",
            "MONSTER ENERGY": "#B195FF",
            "CELSIUS": "#CEC3EF",
            "C4": "#E6DEFC"
        },
        labels={"count_of_reactions": "Reaction Frequency", "name_brand": "Energy Drink Brand"},
        category_orders={"name_brand": brand_order}
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        xaxis=dict(gridcolor="lightgrey", gridwidth = 0.5),
        title_x=0.5
    )
    
    return fig

#Layout
layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                # Left: chart (md=6)
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Reactions by Energy Drink Brand"),
                        dbc.CardBody(
                            dcc.Graph(figure=create_figure())
                        )
                    ]),
                    md=6),
                # Right: reactions (md=6)
                dbc.Col(reactions, md=6),
            ],
            className="g-4",    
        ),
        html.Footer(
            html.Small(
                "Built with Dash. Open data source: openfda.gov (no API key required).",
                className="text-muted",
            ),
            className="mt-3",
        ),
    ],
    fluid=True,
)

#add end notes with source
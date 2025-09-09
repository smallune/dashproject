# AI Assistance: ChatGPT used to to help with API development (manually created).   
# CoPilot used within VSCode was used to help iterate over the
# complicated dictionary dataset. For additional layout syntax assistance, 
# the CoPilot "tab" auto-complete feature was useful. All layout
# elements structured by gen AI were reviewed and revised to
# better suit our project direction.

#Importing packages
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import requests

#Registering the page 
dash.register_page(__name__, path = "/page2", name = "Health Effects")

#Loading in API url  
url = "https://api.fda.gov/food/event.json?search=products.name_brand:%22RED+BULL%22+OR+products.name_brand:%22MONSTER+ENERGY%22+OR+products.name_brand:%225+HOUR%22+OR+products.name_brand:%22BANG%22+OR+products.name_brand:%22C4%22+OR+products.name_brand:%22CELSIUS%22&limit=1000"
r = requests.get(url, timeout = 100)
r.raise_for_status()
results = r.json()["results"]

# Determining what brands, reactions, and outcomes to filter for (might not use outcomes but helpful to have because there is some
# overlap with reactions information) 
energy_drinks_reactions = {
    "name_brand": ["RED BULL", "MONSTER ENERGY", "CELSIUS", "5 HOUR ENERGY", "C4"],
    "reactions": ["Blood pressure","HEART RATE","Dizziness","ANXIETY","NERVOUSNESS","CHEST", "MYOCARDIAL INFARCTION","PALPITATIONS","DYSPNOEA", "STROKE", "CONVULSIONS","LOSS OF CONSCIOUSNESS"],
    "outcomes": ["Hospitalization","Death","Life Threatening"]
}

# Creating a dataframe that consolidates the information from the API
# Ended up taking out outcome and date because not necessary for the visualization 
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

# Make all reactions lowercase to counter capitalization reactions that are counted separately 
filtered_df["reactions"] = filtered_df["reactions"].str.lower()

# Counting every reaction for each brand (used later for dropdown of brands)
brand_reaction_counts = {}
for brand in filtered_df["name_brand"].unique():
    brand_df = filtered_df[filtered_df["name_brand"] == brand]
    reaction_counts = brand_df["reactions"].value_counts().to_dict()
    brand_reaction_counts[brand] = reaction_counts

# Counting total reactions for each brand (used later for graphic) 
total_brand_reactions = {}
for brand in filtered_df["name_brand"].unique():
    total_reactions_per_brand = sum(brand_reaction_counts[brand].values())
    total_brand_reactions[brand] = total_reactions_per_brand

# Creates a dataframe that can be used for the graphic 
total_reactions_df = pd.Series(total_brand_reactions).reset_index()
total_reactions_df.columns = ["name_brand", "count_of_reactions"]

#Top bar (used later in layout)
navbar = html.Div([
   html.H1("Health Effects of Energy Drinks", className = "centered-header") 
])

# Reaction Report Dropdown (right column) (wanted to complete this one first because it had the callback, even though it is in the right column) 
# Shows reactions report associated with specific brand selected in the dropdown menu (to be placed in layout) 
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
                html.Div(id ="reaction-display"),
                html.Hr(),
                html.Small(
                    "Data source: openfda.gov (no API key required).",
                ),
            ])
    ])

# Callback for the reaction dropdown 
@callback(
    Output("reaction-display", "children"),
    Input("brand-dropdown", "value")
)

<<<<<<< HEAD
# Function used in output of dropdown of reactions report 
=======
# Specifically get the reactions output for each brand when selected
>>>>>>> ada948497ba539ab352c4d4a168feb8ce4728ea5
def update_reactions(selected_brand):
    if selected_brand in brand_reaction_counts:
        reactions = brand_reaction_counts[selected_brand]
        reaction_list = [
            html.Li(f"{reaction}: {count} reports")
            for reaction, count in reactions.items()
        ][:5]
        return [
            html.H5(f"Top 5 reactions reported with consuming {selected_brand}:"),
            html.Ul(reaction_list)
        ]
    return "No reactions found for this brand."

<<<<<<< HEAD
# Overall Reaction Barchart Graphic (Left column)
# Note about dates: March 14 2025 was latest date, August 11 2004 was earliest date so categorize as over 20 years
=======
# Barplot (left column)
# March 14 2025 was latest date August 11 2004 (over 20 years)
>>>>>>> ada948497ba539ab352c4d4a168feb8ce4728ea5
brand_order = ["5 HOUR ENERGY", "RED BULL", "MONSTER ENERGY", "CELSIUS", "C4"]
def create_figure():
    fig = px.bar(
        total_reactions_df,
        x="count_of_reactions",
        y="name_brand",
        title="Energy Drink Reactions by Brand",
        color = "name_brand",
        color_discrete_map = {
            "5 HOUR ENERGY": "#424EF7",
            "RED BULL": "#4F6FDA",
            "MONSTER ENERGY": "#4F80DA",
            "CELSIUS": "#4F94DA",
            "C4": "#4F9EDA"
        },
        labels={"count_of_reactions": "Number of total reactions reported per brand", "name_brand": "Energy Drink Brand"},
        category_orders={"name_brand": brand_order}
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        xaxis=dict(gridcolor="lightgrey", gridwidth = 0.5),
        title_x=0.5
    )
    return fig

# Layout which organizes the columns into the right places 
layout = dbc.Container(
    [
        navbar,
        dbc.Row(
            [
                # Left column with graphic (split: md=6)
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Reactions by Energy Drink Brand in the last 20 years (03/11/04 to 08/14/25)"),
                        dbc.CardBody([
                            dcc.Graph(figure=create_figure()),
                            html.Hr(),
                            html.Small(
                                "Note: Common for a medical record to report multiple reactions per person after one instance of consuming the associated energy drink."
                        )
                    ])
            ]),
            md=6),
        # Right column with reactions report (split: md=6)
        dbc.Col(reactions, md=6),
    ],    
),
html.Footer(
    html.Small(
        "Built with Dash. Open data source: openfda.gov (no API key required)."
    )),
],
fluid=True, className="page-padding"
)


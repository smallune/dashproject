#importing packages 
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import requests

#registering the page 
dash.register_page(__name__, path = "/page2", name = "Health Effects")

#add formatting 

#loading in API url and turning it into a dataframe 
url = "https://api.fda.gov/food/event.json?search=products.name_brand:%22RED+BULL%22+OR+products.name_brand:%22MONSTER%22+OR+products.name_brand:%225+HOUR%22+OR+products.name_brand:%22BANG%22+OR+products.name_brand:%22ROCK+STAR%22&limit=1000"
r = requests.get(url, timeout = 30)
r.raise_for_status()
results = r.json()["results"]

#filter what energy drinks and what reactions 
energy_drinks_reactions = {
    "name_brand": ["RED BULL", "MONSTER ENERGY DRINK", "ROCK STAR ENERGY DRINK", "5 HOUR ENERGY DRINK", "BANG ENERGY DRINK"],
    "reactions": ["Blood pressure abnormal","HEART RATE INCREASED","Dizziness","ANXIETY","NERVOUSNESS","CHEST DISCOMFORT", "MYOCARDIAL INFARCTION","PALPITATIONS"]
}

#iterating over url to look at specific filters
records = []
for report in results:
    if "products" in report:
        for product in report["products"]:
            name_brand = product["name_brand"] if "name_brand" in product else ""
            reactions = report["reactions"][0] if "reactions" in report and report["reactions"] else ""
            date_created = report["date_created"] if "date_created" in report else ""
            records.append({
                "name_brand": name_brand,
                "reactions": reactions,
                "date_created": date_created
            })
df = pd.DataFrame(records)

df["year"] = pd.to_datetime(df["date_created"], errors = "coerce").dt.year
#df_energydrinks = df[df["name_brand"].isin(energy_drinks_reactions["name_brand"])]
#df_reactions = df[df["reactions"].isin(energy_drinks_reactions["reactions"])]

filtered_records = [
    row for _, row in df.iterrows()
    if row["name_brand"] in energy_drinks_reactions["name_brand"]
    and row["reactions"] in energy_drinks_reactions["reactions"]
]
filtered_df = pd.DataFrame(filtered_records)

#Top bar
navbar = html.Div([
   html.H1("Health Effects of Caffeinated Drinks", className = "centered-header") 
])

#Left Column (Controls with Dropdown)
layout = html.Div(
    children = [
        navbar,
        html.H4("Select a Brand"),
        dcc.Dropdown(
            id = "brand",
            options = [{"label": b, "value": b} for b in energy_drinks_reactions["name_brand"]],
            value = "RED BULL",
            clearable = False,
            style = {"width": "100%"}),
        dcc.Graph(id="graph")  
], className = "page-padding")


#Reaction count for each name brand 
#def reactions_count(name_brand):
   # reaction_counts = df.groupby("name_brand")["reactions"].value_counts()
   # return reaction_counts

#Chart 
def updated_barchart(selected_brand, filtered_df):
    brand_df = filtered_df[filtered_df["name_brand"] == selected_brand]
    reactions_per_year = brand_df.groupby("year")["reactions"].count().reset_index()
    figure = px.bar(
        reactions_per_year,
        x="year",
        y="reactions",
        title=f"Health Reactions Over Time for {selected_brand}",
        labels={"year": "Year", "reactions": "Number of Reactions"},
        template="plotly_white"
    )
    figure.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Reactions",
        bargap=0.2, #change 
        plot_bgcolor="#f9f9f9" #change 
    )
    return figure

@callback(
    Output("graph", "figure"),
    Input("brand", "value")
)

def update_graph(selected_brand):
    return updated_barchart(selected_brand, filtered_df)

print(filtered_df.head(10))

#add end notes with source
            

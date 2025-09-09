# AI Assistance: Google search AI helped with dash Tabs component.
# AI Assistance: CoPilot helped with the structure of the layout.
# AI Assistance: ChatGPT helped with how to utilize Google Trends API to get regional data.

from dash import html, dcc, Input, Output, callback, register_page
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from pathlib import Path
from pytrends.request import TrendReq

register_page(__name__, path = '/page3', name = 'Demographics')

pytrends = TrendReq(hl='en-US', tz=360)

# US region mapping data
# Downloaded from https://gist.github.com/rogerallen/1583593 then save to csv file
DataPath = Path(__file__).resolve().parent.parent / 'data' / 'us_region_mapping.csv'
df_us_region_mapping = pd.read_csv(DataPath)

layout = html.Div(
    className = 'page-padding',
    children = [
    html.H2("Demographic Data", className = "centered-header"),
    dcc.Tabs(id="tab_product", value='Red Bull', children=[
        dcc.Tab(label = 'Red Bull', value = 'Red Bull'),
        dcc.Tab(label = 'Monster', value = 'Monster'),
        dcc.Tab(label = 'Rockstar', value = 'Rockstar'),
        dcc.Tab(label = '5-hour Energy', value = '5-hour Energy'),
        dcc.Tab(label = 'Bang', value = 'Bang')
    ]),
    dcc.Slider(
        id = 'year-slider',
        min = 2015,
        max = 2025,
        value = 2025,
        marks = {
            str(y): str(y) for y in range(2015, 2026)
        },
        step = None,
        tooltip = {'placement': 'bottom', 'always_visible': True}
    ),
    html.Br(),
    html.Div(id = 'choropleth-map') 
])

@callback (
    Output('choropleth-map', 'children'),
    Input('tab_product','value'),
    Input('year-slider', 'value'),
)
    
def update_map_trends(brand, selected_year):
    # Get data from Google Trends
    # Specify the timeframe from the selected year with slider
    time_range = f'{selected_year}-01-01 {selected_year}-12-31'
    error_message = ''
    
    # Sometimes Google Trends API fails, so we will use downloaded data instead. Because it detects as too many requests from the same IP.
    try:
        pytrends.build_payload([brand], cat=0, timeframe= time_range, geo='US', gprop='')
        df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    except Exception as e:
        # Catch any other unexpected errors
        error_message = f"Acutally an unexpected error occurred: {e}. We are using downloaded data instead."
        # Remove ' Energy Drink' word to match the file names
        brand = brand.replace(' Energy Drink', '')
        df = pd.read_csv(f'data/gg_trends/{selected_year}/{selected_year}_{brand}.csv')
        df = df.iloc[1:]
    
    # Clean dataframe
    df = df.reset_index()
    df['year'] = selected_year
    df.columns = ['region', 'Interest over time', 'year']
    df = pd.merge(df, df_us_region_mapping, left_on='region', right_on = 'region_name', how='left')
    df = df[['region_code', 'Interest over time', 'year']]
    df['Interest over time'] = df['Interest over time'].fillna(0)
    df['Interest over time'] = df['Interest over time'].replace('<', '')
    df['Interest over time'] = df['Interest over time'].astype('int64')
        
    fig = px.choropleth(
        df,
        locations = 'region_code',
        locationmode = 'USA-states',
        color = 'Interest over time',
        scope = 'usa',
        color_continuous_scale = 'PuBu',
        labels = {'price': 'Price (cents/kWh)'},
        title = f'Interest in {brand} over {selected_year} - Data source: Google Trends {error_message}'
    )
    fig.update_layout(
        geo = dict(), ## background color around map
        # paper_bgcolor = '#113631',
        # font_color = '#ffffff',
        margin = dict(l = 10, r = 10, t = 50, b = 20)   
    )
    return dcc.Graph(figure=fig)

    
# add end notes with sources
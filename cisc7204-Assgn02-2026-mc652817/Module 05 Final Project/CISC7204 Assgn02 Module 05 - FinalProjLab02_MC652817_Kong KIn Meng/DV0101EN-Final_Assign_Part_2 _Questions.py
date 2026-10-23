#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas (teacher's original data source).
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years: retained from the teacher's supplied template.
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value=None,
            placeholder='Select Statistics',
            clearable=False,
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px'}
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value=None,
        placeholder='Select-year',
        disabled=True,
        clearable=False
    )),
    # TASK 2.3: Add a division for output display
    html.Div([
        html.Div(id='output-container', className='chart-grid',
                 style={'display': 'flex', 'flexDirection': 'column'})
    ])
])

# TASK 2.4: Creating Callbacks
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # TASK 2.5: Create and display graphs for Recession Report Statistics
        # Plot 1: Average automobile sales by recession year
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(
            yearly_rec, x='Year', y='Automobile_Sales',
            title='Average Automobile Sales fluctuation over Recession Period'))

        # Plot 2: Average vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(
            average_sales, x='Vehicle_Type', y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type during Recessions'))

        # Plot 3: Total advertising expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(
            exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
            title='Advertising Expenditure Share by Vehicle Type during Recessions'))

        # Plot 4: Unemployment rate, vehicle type and average sales
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(
            unemp_data, x='unemployment_rate', y='Automobile_Sales',
            color='Vehicle_Type', barmode='group',
            labels={'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'},
            title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart1, style={'width': '50%', 'minWidth': 0}),
                html.Div(children=R_chart2, style={'width': '50%', 'minWidth': 0})
            ], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[
                html.Div(children=R_chart3, style={'width': '50%', 'minWidth': 0}),
                html.Div(children=R_chart4, style={'width': '50%', 'minWidth': 0})
            ], style={'display': 'flex'})
        ]

    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly average sales for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas, x='Year', y='Automobile_Sales',
            title='Average Yearly Automobile Sales for the Whole Period'))

        # Plot 2: Monthly total sales for the SELECTED year.
        # Corrects the template's use of data instead of yearly_data.
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(
            mas, x='Month', y='Automobile_Sales',
            title='Total Monthly Automobile Sales in {}'.format(input_year)))

        # Plot 3: Average vehicles sold by vehicle type for the selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        # Plot 4: Total advertising expenditure share for the selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
            title='Advertising Expenditure by Vehicle Type in {}'.format(input_year)))

        # Return two rows of two graphs, as in the teacher's template.
        return [
            html.Div(className='chart-item', children=[
                html.Div(children=Y_chart1, style={'width': '50%', 'minWidth': 0}),
                html.Div(children=Y_chart2, style={'width': '50%', 'minWidth': 0})
            ], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[
                html.Div(children=Y_chart3, style={'width': '50%', 'minWidth': 0}),
                html.Div(children=Y_chart4, style={'width': '50%', 'minWidth': 0})
            ], style={'display': 'flex'})
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=False, port=8051)

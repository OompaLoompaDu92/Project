from dash import dcc, html, Dash, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime


# Create a function to calculate the daily metrics
def calculate_daily_metrics(datavalue):
    # Get today's date
    today = datetime.date.today()

    # Filter the data to get today's values
    today_data = datavalue[datavalue['date'] == str(today)]

    # Calculate the metrics
    daily_volatility = today_data['index_value'].pct_change().std()
    price = today_data['index_value'].iloc[-1]
    evolution = (price - today_data['index_value'].iloc[0]) / today_data['index_value'].iloc[0]
    open_price = today_data['index_value'].iloc[0]
    close_price = today_data['index_value'].iloc[-1]

    # Return the metrics as a dictionary
    return {
        'Date': str(today),
        'Daily Volatility': round(daily_volatility, 4),
        'Price': round(price, 2),
        'Evolution': round(evolution, 4),
        'Open': round(open_price, 2),
        'Close': round(close_price, 2)
    }

# Create the layout of the dashboard
app = Dash()
app.layout = html.Div(children=[
    html.H1('FTSE 100'),
    html.P('Here is my dashboard scrapping the value of the stock index FTSE 100'),
    html.P('Set up to reflect developments on the London stock Exchange'),
    dcc.Graph(id='graph'),
    html.H2('Daily Report'),
    dash_table.DataTable(
    id='table',
    columns=[{'name': col, 'id': col} for col in ['Date', 'Daily Volatility', 'Price', 'Evolution', 'Open', 'Close']],
    data=[],
    style_table={'overflowX': 'scroll'},
    style_cell={
        'textAlign': 'center',
        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
    },
    style_header={
        'fontWeight': 'bold'
    },
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*60*1000, # Refresh interval in milliseconds
        n_intervals=0
    )
])

# Define a function to update the dashboard
def update_dashboard(n):
    # Update the graph
    datavalue = pd.read_csv('/home/admin/FTSE100_VALUE.txt', sep=',')
    figure = {
        'data': [
            {'x': datavalue['time'], 'y':datavalue['index_value'],'type':'scatter','name': 'Data'}
        ],
        'layout': {

            'title': 'Evolution of the FTSE100',
            'xaxis': {
                'tickmode': 'array',
                'tickvals': [datavalue['time'][i] for i in range(len(datavalue['time'])) if pd.to_datetime(datavalue['time'][i]).minute == 0],
                'tickformat': '%H:%M'
            },
        }

    }

    # Update the daily report
    now = datetime.datetime.now().time()
    if now.hour >= 20:
        daily_metrics = calculate_daily_metrics(datavalue)
        data = [daily_metrics]
    else:
        data=[]

    # Return the updated dashboard components
    return figure, data

# Create a callback that updates the dashboard at the specified interval
@app.callback(
    [Output('graph', 'figure'), Output('table', 'data')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard_callback(n):
    figure, data = update_dashboard(n)
    return figure,data

# Run the Dash app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050,debug=True)

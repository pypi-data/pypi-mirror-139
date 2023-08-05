import math
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from dash.dependencies import Input, Output
from dash import html
from dash import dcc

from inspec_ai._datasets.occupancy import room_occupancy

occupancy = room_occupancy()

app = dash.Dash(__name__)

df = occupancy

x = df["date"]

all_y = df.drop(columns=x.name)

df_col_amount = all_y.shape[1]

row_amount = math.floor(df_col_amount / 2) + 1
col_amount = 2

specs= [[{"rowspan": 2, "colspan": 2}, None],
           [None, None]]
for i in range(1, row_amount):
    row = []
    for j in range(0, 2):
        row.append({})

    specs.append(row)


fig = make_subplots(rows=row_amount + 1, 
                    cols=col_amount,
                    shared_xaxes="all",
                    specs=specs)

fig.add_trace(go.Scatter(x=x, y=all_y[all_y.columns[0]], name=all_y.columns[0]),
              row=1, col=1)

index = 1
for i in range(1, row_amount):
    for j in range(0, col_amount):
        if index < df_col_amount:
            fig.add_trace(go.Scatter(x=x, y=all_y[all_y.columns[index]], name=all_y.columns[index]),
                row=(i + 2), col=(j + 1))

        index = index + 1

fig.update_yaxes(fixedrange=True)
fig.update_xaxes(matches='x')

tabs = ['tab-1-example-graph', 'tab-2-example-graph']

current_tab = tabs[0]

app.layout = html.Div([
    html.H1(children="InSpec"),
    html.Div(children="""
        Prototype: Summary
    """),
    html.Button(id="tab-button", children="Change tab"),
    dcc.Tabs(id="tabs-example-graph", value=current_tab, children=[
        dcc.Tab(label='Subplots', value=tabs[0]),
        dcc.Tab(label='Bar Chart', value=tabs[1]),
    ]),
    html.Div(id='tabs-content-example-graph')
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            dcc.Graph(
                id="subplots-graph",
                figure=fig
            )
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])


@app.callback(Output('tabs-example-graph','value'), 
              Input('tab-button','n_clicks'))
def display_newtab(n_clicks):
    global current_tab

    if current_tab == tabs[0]:
        current_tab = tabs[1]
    else:
        current_tab = tabs[0]

    return current_tab

if __name__ == "__main__":
    app.run_server(debug=True)

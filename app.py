# This is a test for git
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import pandas as pd

import metric_calculations as mc
import build_data

app = dash.Dash()

# raw_data = pd.read_csv('data/cover-output-1506343018603.csv')
raw_data = build_data.create_sample_df(1000)
roc_data = mc.build_roc_data(raw_data)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


table = html.Div(children=[
    html.H4(children='Assurance Scoring Threshold Explorer'),
    generate_table(roc_data)
])


graph = dcc.Graph(
    id='roc-curve',
    figure={
        'data': [
            go.Scatter(
                x=roc_data['FPR'],
                y=roc_data['TPR'],
                text='hello world',
                mode='lines+markers',
                opacity=0.7,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
            )
        ],
        'layout': go.Layout(
            xaxis={'type': 'linear', 'title': 'FPR'},
            yaxis={'title': 'TPR'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
)


slider = dcc.Slider(
    id='slider',
    value=0.5,
    min=0.0,
    max=1.0,
    step=0.01,
    marks={i/10: '{}'.format(i/10) for i in range(0, 10)}
)


tags = dcc.Dropdown(
    options=[{'label': c, 'value': c} for c in raw_data.columns],
    value=['score', 'class'],
    multi=True
)


app.layout = html.Div([
    tags,
    graph,
    table,
    slider,
    html.Div(id='threshold'),
])


@app.callback(
    Output(component_id='threshold', component_property='children'),
    [Input(component_id='slider', component_property='value')]
)
def update_text(input_value):
    return 'Threshold: "{}"'.format(input_value)




if __name__ == '__main__':
    app.run_server()

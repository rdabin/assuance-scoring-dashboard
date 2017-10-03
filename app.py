import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd
import os.path
import flask
import os

# from graph import graph
# from table import table
import metric_calculations as mc
import methods as mt
import build_data as bd


STATIC_ROUTE = 'static'
STATIC_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    STATIC_ROUTE
)


TP_COLOUR = '#e03344'
FP_COLOUR = '#ef7b28'
TN_COLOUR = '#09ef33'
FN_COLOUR = '#aabf22'

TP_TEXT = 'hit'
FP_TEXT = 'false alarm'
TN_TEXT = 'meh'
FN_TEXT = 'miss'

# define some parameters for histogram
resolution = 4  # number of points per 10 - this is not working properly
bins1 = 40  # number of bins on histogram data
step = 1 / bins1  # for the slider, to make step same size as histogram bins
point_size = 10  # data point size for the histogram plot


# Load data
# datafile = 'data/data.csv'
# if not os.path.isfile(datafile):
#     raw_data = build_data.create_sample_datafile(num_records=1000, datafile)
# else:
#     raw_data = pd.read_csv(datafile)
raw_data = bd.create_sample_df()

# calculate roc data
roc_data = mc.build_roc_data(raw_data)


# create graph divs

slider = html.Div([
    dcc.Slider(
        id='slider',
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.01,
        updatemode='drag',
        # vertical=True,
        # marks={i / 10.0: '{}'.format(i / 10.0) for i in range(0, 11)},
        marks={i / 10: '{}'.format(i / 10) for i in range(0, 11)},
    )],
    style={
        'width': '100%',
        'display': 'inline-block',
        'padding-top': '20px',
        'padding-bottom': '20px'
    }
)


def get_roc_graph(roc_data):

    line = go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        #opacity=0.7,
        line=dict(
            color=('rgb(180, 180, 180)'),
            width=1,
            dash='dash',   # dash options include 'dash', 'dot', and 'dashdot'
        )
    )

    curve = go.Scatter(
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

    return html.Div([
            dcc.Graph(
                id='roc-curve',
                config={'displayModeBar': False},
                figure={
                    'data': [
                        curve,
                        line
                    ],
                    'layout': go.Layout(
                        showlegend=False,
                        xaxis={'type': 'linear', 'title': 'FPR'},
                        yaxis={'title': 'TPR'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )],
        style={'width': '48%', 'display': 'inline-block'}
    )


roc_graph = get_roc_graph(roc_data)


def get_cost_graph(roc_data):

    curve = go.Scatter(
        x=roc_data['threshold'],
        y=roc_data['cost'],
        text='hello world',
        mode='lines+markers',
        opacity=0.7,
        marker={
            'size': 5,
            'line': {'width': 0.5, 'color': 'white'}
        },
    )

    return html.Div([
        dcc.Graph(
            id='cost-curve',
            config={'displayModeBar': False},
            figure={
                'data': [
                    curve
                ],
                'layout': go.Layout(
                    showlegend=False,
                    xaxis={'type': 'linear', 'title': 'threshold'},
                    yaxis={'title': 'cost'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )],
        style={'width': '48%', 'display': 'inline-block'}
    )


def generate_bar_of_dots(c1=100, c2=16, width=15):
    return pd.DataFrame([
        {
            'type': 0 if i < c1 else 1,
            'x': i % width,
            'y': i // width,
        } for i in range(0, c1 + c2)
    ])


dots = generate_bar_of_dots()

volume_layout = go.Layout(
            width=315,
            # height=300,
            showlegend=False,
            hovermode=False,
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange='reversed',
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            )
        )

# volume = html.Div([
volume1 = dcc.Graph(
        id='volume1',
        config={'displayModeBar': False},
        figure={
            'data': [
                go.Scatter(
                    x=dots[dots['type'] == dot_type]['x'],
                    y=dots[dots['type'] == dot_type]['y'],
                    text='foo',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=dot_type
                ) for dot_type in dots['type'].unique()
            ],
            'layout': volume_layout
        }
    )
    # ],
    # style={'width': '20%', 'display': 'inline-block'})

volume2 = dcc.Graph(
        id='volume2',
        config={'displayModeBar': False},
        figure={
            'data': [
                go.Scatter(
                    x=dots[dots['type'] == dot_type]['x'],
                    y=dots[dots['type'] == dot_type]['y'],
                    text='foo',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=dot_type
                ) for dot_type in dots['type'].unique()
            ],
            'layout': volume_layout
        }
    )

pie_chart = dcc.Graph(
    id='pie_chart',
    config={'displayModeBar': False},
)

histogram = dcc.Graph(
    id='histogram',
    config={'displayModeBar': False},
)

cost_graph = get_cost_graph(roc_data)


# initialise app

app = dash.Dash()

# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


app.layout = html.Div([
    html.Div(
        [
            html.Div([
                html.Img(
                    id='logo',
                    src=os.path.join(STATIC_ROUTE, "homeoffice.png"),
                    style={'width': '60px', 'height': '60px', 'float': 'left'}
                ),
                html.H2(children='HODAC threshold explorer', style={'padding-top': '1rem'}),
                html.Div([slider], className='twelve columns'),
            ], className='row'),
            html.Div(
                id='threshold',
                style={'font-size': '16pt', 'padding-top': '10px', 'font-weight': 'bold'},
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='hist_with_slider',
                        config={'displayModeBar': False},
                        animate=False
                    )
                ], className='six columns'),
                html.Div([volume1], className='three columns'),
                html.Div([volume2], className='three columns')
            ], className='row')
        ],
        id='grid'
    ),
    pie_chart,
    histogram,
    roc_graph,
    cost_graph
], style={})


# add static image server
@app.server.route(os.path.join('/', STATIC_ROUTE, '<filename>'))
def serve_static(filename):
    return flask.send_from_directory(STATIC_PATH, filename)


app.css.append_css({
    'external_url': 'static/site.css',
})


# callbacks

@app.callback(
    dash.dependencies.Output('hist_with_slider', 'figure'),
    [dash.dependencies.Input('slider', 'value')])
def update_histogram(threshold):
    """
    Update histogram coloring according to slider threshold

    """
    hist_exp, bins_exp, colors_exp = mt.histogram_data(raw_data, threshold, resolution, bins1,
        TP_COLOUR = TP_COLOUR, FP_COLOUR = FP_COLOUR, TN_COLOUR = TN_COLOUR, FN_COLOUR = FN_COLOUR)
    figure = {
        'data': [
            go.Scatter(
                x=bins_exp,
                y=hist_exp,
                text='Histogram',
                mode='markers',
                # opacity=0.7,
                marker={
                    'size': point_size,
                    'color': colors_exp,
                    'line': {'width': 0.5, 'color': 'white'}
                },
            )
        ],
        'layout': go.Layout(
            width=600,
            height=300,
            xaxis={'type': 'linear', 'title': 'Threshold'},
            yaxis={'title': 'Counts'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure


# @app.callback(
#     Output(component_id='threshold', component_property='children'),
#     #[Input(component_id='slider', component_property='value')]
#     [Input(component_id='hist_with_slider', component_property='hoverData')]
# )
# def update_text_graph(input_value):
#     hover_data = input_value['points'][0]
#     print(hover_data)
#     print(type(hover_data))
#     for key in hover_data.keys():
#         print(key)
#     threshold = hover_data['x']
#     print(threshold)
#     return 'Threshold: "{}"'.format(threshold)




@app.callback(Output('volume1', 'figure'),
              [Input('slider', 'value')])
def make_volume1(slider):

    tp, fp, tn, fn = mc.confusion_matrix(raw_data, slider)
    sz = len(raw_data)
    grid_rows = 20
    grid_columns = 15
    grid_total_dots = grid_columns * grid_rows
    c1 = int(tp * grid_total_dots / sz)
    c2 = int(tn * grid_total_dots / sz)
    dots = generate_bar_of_dots(c1=c1, c2=c2, width=grid_columns)
    grid_width = 315
    dot_spacing = int(grid_width / grid_columns)

    data = [
        go.Scatter(
            x=dots[dots['type'] == dot_type]['x'],
            y=dots[dots['type'] == dot_type]['y'],
            text='foo',
            mode='markers',
            # opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'},
                'color': TP_COLOUR if dot_type == 0 else TN_COLOUR,
            },
            name=dot_type
        ) for dot_type in dots['type'].unique()
    ]

    figure = dict(
        data=data,
        layout=go.Layout(
            width=grid_width,
            height=grid_rows * dot_spacing,
            showlegend=False,
            hovermode=False,
            xaxis=dict(
                fixedrange=True,
                range=[-1, grid_columns],
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                fixedrange=True,
                range=[grid_rows, -1],
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            )
        )
    )

    return figure


@app.callback(Output('volume2', 'figure'),
              [Input('slider', 'value')])
def make_volume2(slider):

    tp, fp, tn, fn = mc.confusion_matrix(raw_data, slider)
    sz = len(raw_data)
    grid_rows = 20
    grid_columns = 15
    grid_total_dots = grid_columns * grid_rows
    c1 = int(fp * grid_total_dots / sz)
    c2 = int(fn * grid_total_dots / sz)
    dots = generate_bar_of_dots(c1=c1, c2=c2, width=grid_columns)
    grid_width = 315
    dot_spacing = int(grid_width / grid_columns)

    data = [
        go.Scatter(
            x=dots[dots['type'] == dot_type]['x'],
            y=dots[dots['type'] == dot_type]['y'],
            text='foo',
            mode='markers',
            # opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'},
                'color': FP_COLOUR if dot_type == 0 else FN_COLOUR,
            },
            name=dot_type
        ) for dot_type in dots['type'].unique()
    ]

    figure = dict(
        data=data,
        layout=go.Layout(
            width=grid_width,
            height=grid_rows * dot_spacing,
            showlegend=False,
            hovermode=False,
            xaxis=dict(
                fixedrange=True,
                range=[-1, grid_columns],
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                fixedrange=True,
                range=[grid_rows, -1],
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            )
        )
    )

    return figure


@app.callback(Output('pie_chart', 'figure'),
              [Input('slider', 'value')])
def make_pie_figure(slider):

    tp, fp, tn, fn = mc.confusion_matrix(raw_data, slider)

    data = [
        dict(
            type='pie',
            ids=['TP', 'FN'],
            labels=['True positive', 'False negative'],
            values=[tp, fn],
            text=[TP_TEXT, FN_TEXT],
            hoverinfo='value',
            name='Recall',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0, 0.4], 'y':[0.6, 1]},
            marker=dict(colors=[TP_COLOUR, FN_COLOUR]),
            # Haven't been able to get this annotation to work yet
            # annotations=[dict(text='Recall', x=0.2, y=0.9, xref='paper', yref='paper')]
        ),
        dict(
            type='pie',
            ids=['TP', 'FP'],
            labels=['True positive', 'False positive'],
            values=[tp, fp],
            hoverinfo='value',
            text=[TP_TEXT, FP_TEXT],
            name='Precision',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0.6, 1], 'y':[0.6, 1]},
            marker=dict(colors=[TP_COLOUR, FP_COLOUR])
        ),
        dict(
            type='pie',
            ids=['TP', 'TN', 'FP', 'FN'],
            labels=[
                'True positive',
                'True negative',
                'False positive',
                'False negative'
            ],
            values=[tp, tn, fp, fn],
            text=[TP_TEXT, TN_TEXT, FP_TEXT, FN_TEXT],
            hoverinfo='value',
            name='Accuracy',
            pull=[0, 0, 0.1, 0.1],
            hole=0.5,
            sort=False,
            domain={"x": [0, 0.4], 'y':[0, 0.4]},
            marker=dict(colors=[TP_COLOUR, TN_COLOUR, FP_COLOUR, FN_COLOUR])
        ),
        dict(
            type='pie',
            ids=['FP', 'TN'],
            labels=['False positive', 'True negative'],
            values=[fp, tn],
            text=[FP_TEXT, TN_TEXT],
            hoverinfo='value',
            name='False positive rate',
            pull=[0.1, 0],
            hole=0.5,
            sort=False,
            domain={"x": [0.6, 1], 'y':[0, 0.4]},
            marker=dict(colors=[FP_COLOUR, TN_COLOUR])
        )
    ]

    figure = dict(
        data=data,
        layout=dict(
            autosize=True,
            showlegend=False,
            title='Confusion Matrix Explanation'
        )
    )

    return figure


@app.callback(Output('histogram', 'figure'),
              [Input('slider', 'value')])
def make_histogram(slider):

    TP, FP, TN, FN = mc.confusion_matrix(raw_data, slider)

    figure = go.Figure(
        data=[
            go.Bar(
                x=['TP', 'FP', 'TN', 'FN'],
                y=[TP, FP, TN, FN],
                marker=dict(
                    color=[TP_COLOUR, TN_COLOUR, FP_COLOUR, FN_COLOUR],
                    line=dict(
                        color='rgb(8,48,107)',
                    )
                )
            )
        ],
        layout=dict(
            width=300,
            height=400,
            autosize=True,
            showlegend=False,
            #hovermode=False,
            #title='Confusion Matrix Explanation2'
        )
    )

    return figure


@app.callback(
    Output(component_id='threshold', component_property='children'),
    [Input(component_id='slider', component_property='value')]
)
def update_text(input_value):
    return 'threshold={}'.format(input_value)
#    return input_value


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server()

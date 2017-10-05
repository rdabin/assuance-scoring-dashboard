import dash
import json
from src.graph import graph
from src.table import table
from src.metrics_calculator import metrics_calculator
from src.data_builder import data_builder
from src.callback_manager import callback_manager
from src.volume_plot import volume_plot
from src.slider import slider

from src.pie_chart.pie_chart import Pie_Chart

# TODO: imports to remove once refactored callbacks etc into modules
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


with open('config.json') as config_json: 
    config = json.load(config_json)


# Load data
raw_data = data_builder.create_sample_df()

# calculate roc data
roc_data = metrics_calculator.build_roc_data(raw_data)


# create graphs
slider = slider.get()

my_pie = Pie_Chart('pie_chart', raw_data, config["confusion_matrix"])
pie_chart = my_pie.get()
# histogram = dcc.Graph(id='histogram')
# roc_graph = graph.get_graph(roc_data)
# volume_plot = volume_plot.get_population_dots()
# cost_graph = graph.get_cost_graph(roc_data)



# initialise app
app = dash.Dash()
# TODO: spike offline static content (css, js, images)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.layout = html.Div([
    html.H4(children='HODAC Threshold Explorer'),
    slider,
    # roc_graph,
    # volume_plot,
    pie_chart
    # histogram,
    # cost_graph
])


##REGISTER CONTROLLER CALLBACKS
# my_visulisations = [(slider, my_pie)]

callback_manager.register_callbacks(app, my_pie) # my_visulisations)


if __name__ == '__main__':
    app.run_server()


























# TODO: move to modules
# @app.callback(Output('histogram', 'figure'), [Input('slider', 'value')])
# def make_histogram_figure(slider):

#     TP, FP, TN, FN = metrics_calculator.confusion_matrix(df, slider)

#     figure = go.Figure(
#         data=[
#             go.Bar(
#                 x=['TP', 'FP', 'TN', 'FN'],
#                 y=[TP, FP, TN, FN],
#                 name='My Bar Chart'
#             )
#         ]
#     )

#     return figure

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

agricultural_data = pd.read_csv('usa-agricultural-exports-2011.csv')

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
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(agricultural_data)
])

gdp_life_exp_data = pd.read_csv('gdp-life-exp-2007.csv')
graph = dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=gdp_life_exp_data[gdp_life_exp_data['continent'] == i]['gdp per capita'],
                    y=gdp_life_exp_data[gdp_life_exp_data['continent'] == i]['life expectancy'],
                    text=gdp_life_exp_data[gdp_life_exp_data['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in gdp_life_exp_data.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )

slider = dcc.Slider(value=4, min=-10, max=20, step=0.5,
           marks={-5: '-5 Degrees', 0: '0', 10: '10 Degrees'})

app.layout = html.Div([
    graph,
    table,
    slider
])

if __name__ == '__main__':
    app.run_server()

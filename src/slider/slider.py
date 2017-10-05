import dash_html_components as html
import dash_core_components as dcc


def get():
	
	return html.Div([
	    dcc.Slider(
	        id='slider',
	        value=0.5,
	        min=0.0,
	        max=1.0,
	        step=0.01,
	        marks={i/10: '{}'.format(i/10) for i in range(0, 10)}
	    )],
	    style={'width': '48%', 'display': 'inline-block'}
	)
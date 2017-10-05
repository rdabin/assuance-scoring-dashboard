from dash.dependencies import Input, Output

def register_callbacks(app, pie_chart):

	@app.callback(Output(pie_chart.id, 'figure'), [Input('slider', 'value')])
	def update_pie(slider_value):

		return pie_chart.make_pie_figure(slider_value)

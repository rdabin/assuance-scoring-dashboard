import dash_core_components as dcc
from src.metrics_calculator import metrics_calculator


class Pie_Chart(object):

	def __init__(self, id, data, config):

		self.id = id
		self.data = data
		self.config = config


	def get(self):
		return dcc.Graph(id=self.id)


	# @app.callback(Output('pie_chart', 'figure'), [Input('slider', 'value')])
	def make_pie_figure(self, slider_value):

		true_positive, false_positive, true_negative, false_negative = metrics_calculator.confusion_matrix(self.data, slider_value)
		
		recall = self.get_pie_configuration('Recall', [
    		self.get_segment_definition('true_positive', true_positive),
    		self.get_segment_definition('false_negative', false_negative)
    	])

		precision = self.get_pie_configuration('Precision', [
    		self.get_segment_definition('true_positive', true_positive),
    		self.get_segment_definition('false_positive', false_positive)
    	])

		accuracy = self.get_pie_configuration('Accuracy', [
			self.get_segment_definition('true_positive', true_positive),
			self.get_segment_definition('true_negative', true_negative),
			self.get_segment_definition('false_positive', false_positive),
			self.get_segment_definition('false_negative', false_negative)
    	])

		false_positive_rate = self.get_pie_configuration('False positive rate', [
			self.get_segment_definition('false_positive', false_positive),
			self.get_segment_definition('true_negative', true_negative)
    	])
		
	
		return dict(data=[ recall, precision, accuracy, false_positive_rate ], layout=dict(autosize=True, title='Confusion Matrix Explanation'))


	def get_segment_definition(self, metric_type, metric_value):

		type_split = metric_type.split("_")
		label = " ".join([ i.title() for i in type_split])
		id = "".join([ i[0].upper() for i in type_split])

		return {
	    	"label": label,
	    	"id": id,
	    	"value": metric_value,
	    	"text": self.config[metric_type]["text"],
	    	"colour": self.config[metric_type]["colour"]
	    }


	def get_pie_configuration(self, name, data):

		return dict(
	        type='pie',
	        ids=[ item["id"] for item in data ],
	        labels=[ item["label"] for item in data ],
	        values=[ item["value"] for item in data ],
	        text=[ item["text"] for item in data ],
	        hoverinfo='value',
	        name=name,
	        pull=[0.1, 0],
	        hole=0.5,
	        sort=False,
	        domain={"x": [0, 0.4], 'y':[0.6, 1]},
	        marker=dict(colors=[ item["colour"] for item in data ])
	    )
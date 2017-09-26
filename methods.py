
import pandas as pd
import numpy as np

def round_res (vals, resolution):
	#assert(isinstance(vals, list)), "Input should be a list"
	vals_rd = [ np.round (value / resolution) for value in vals]
	return vals_rd

def bar_coordinates(hista, threshold, binsa,  resolution, acc,
	TP_COLOUR = '#e03344',FP_COLOUR = '#ef7b28',TN_COLOUR = '#09ef33',FN_COLOUR = '#aabf22'):
	

	hist_exp1 = []
	bins_exp1 = []
	colors_1 = []
	colors_2 = []
	#Get the counts for each class for each column on the histogram
	target_acc = acc.score.as_matrix()

	# create this as a percentage
	target_hist = []
	print(binsa)

	for cnt in range(0,len(target_acc),2):
		target_hist.append( (target_acc[cnt]/ ( target_acc[cnt] + target_acc[cnt+1])))

	#round up values first
	# Generate colors accoriding to target
	cnt = 0
	step =1/len(binsa)

	for value, x in zip(hista,binsa[1:]):
		no_points = int(value //10  +1) * resolution
		y_points = np.arange(0,value,value/no_points)+ 1
		x_points = (x-step/2)*np.ones(no_points)
		class_0 =  int(round(no_points*target_hist[cnt]))
		class_1 = no_points - class_0
		# create the colors based on the thresold
		print(x)
		if x >=threshold:
			print('color1')
			colors1 = [[FP_COLOUR for c in range(class_0)], [TP_COLOUR for c in range(class_1)]]
		else:
			print('color2')
			colors1 = [[FN_COLOUR for c in range(class_0)], [TN_COLOUR for c in range(class_1)]]
		cnt = cnt+1
		hist_exp1.append([y for y in y_points])
		bins_exp1.append([x1 for x1 in x_points])
		colors_1.append(colors1)


	# Unnest the lists
	hist_exp  = [val for sublist in hist_exp1 for val in sublist]
	bins_exp  = [val for sublist in bins_exp1 for val in sublist]
	colors_exp  = [val for sublist in colors_1 for val in sublist]
	colors_exp  = [val for sublist in colors_exp for val in sublist]



	# COnvert to np arrays for plotting
	bins_exp = np.asarray(bins_exp)
	hist_exp = np.asarray(hist_exp)
	colors_exp = np.asarray(colors_exp)


	return hist_exp, bins_exp, colors_exp


def histogram_data(input_df, threshold, resolution, bins, target_col = 'class', score_col = 'score'):
	df = input_df.copy()
	hista, binsa = np.histogram(df[score_col], bins = bins, range = [0,1])
	df['cat']= pd.cut(df[score_col], binsa)
	acc =  df[['cat',target_col,score_col]].groupby(['cat',target_col]).count()
	
	# Get now the data to plot 
	# -> for a bar of size 2, we want for exampole to create 8 vertical coordinates

	hist_exp, bins_exp, colors_exp= bar_coordinates(hista, threshold, binsa, resolution, acc)

	return hist_exp, bins_exp, colors_exp
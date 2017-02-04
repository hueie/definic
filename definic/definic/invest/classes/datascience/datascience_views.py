from django.shortcuts import render
from .datascience_forms import RegressionForm
from .datascience_models import	RegressionModel

from chartit import DataPool, Chart
from .regression import LinearRegressionModel
from .preprocessor import Preprocessor
from ..backstage.datawarehouse import DataWareHouse
import numpy as np
import pandas as pd

def	machinelearning(request):
	mainmenu = "datascience"
	submenu = "machinelearning"
	maintitle="datascience"
	subtitle="machinelearning"
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,}
	return render(request, 'index.html', context)

def	regression(request):
	mainmenu = "datascience" ; submenu = "regression"
	maintitle="datascience" ; subtitle="regression"

	datawarehouse = DataWareHouse()
	stockcodelst = datawarehouse.selectAllStockCodeFromDB()
	stockcodetop = datawarehouse.selectTopStockCodeFromDB()
	stock_code = (list(stockcodetop)[0])['stock_code']
	
	if request.method == 'GET':
		form = RegressionForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStockcode']
			if(pStockCode != ""):
				stock_code = pStockCode
	elif request.method == 'POST':
		pass
	
	data = datawarehouse.selectYahooDataFromDB(stock_code)
	preprocessor = Preprocessor()
	train, test = preprocessor.splitDataset(data, 0.8)

	x_train = np.array([ [row] for row in train['open'] ])
	y_train = np.array(train['adj_close'])
	x_test = np.array([ [row] for row in test['open'] ])
	y_test = np.array(test['adj_close'])

	linearregression = LinearRegressionModel()
	print("Linear Regression Start")    
	print("Train : ", linearregression.train( x_train, y_train))
	y_pred = linearregression.predict( x_test)
	print("Y_true : ", y_test)
	print("Predicted : ", y_pred)
	print("Score : ", linearregression.score(x_test, y_test))
	print("Hit Ratio : ", linearregression.hitRatio(y_test, y_pred))
	print("meanSquaredError : ", linearregression.meanSquaredError(y_test, y_pred))
	test['predicted_data'] = pd.DataFrame(data=y_pred, index=test.index)
	
	RegressionModel.objects.all().delete()
	if	RegressionModel.objects.count() == 0:
		for row_idx in range(data.shape[0]):
			RegressionModel.objects.create(
				Stock_code = data.loc[row_idx, 'stock_code'], 
				Date = data.loc[row_idx, 'date'], 
				Lst_reg_dt = data.loc[row_idx, 'lst_reg_dt'], 
				Open = data.loc[row_idx, 'open'], 
				High = data.loc[row_idx, 'high'], 
				Low = data.loc[row_idx, 'low'], 
				Close = data.loc[row_idx, 'close'], 
				Volume = data.loc[row_idx, 'volume'],
				Adj_Close = data.loc[row_idx, 'adj_close'],
				Predicted_data = data.loc[row_idx, 'adj_close']
				)
	
	for row_idx in range(test.shape[0]):
		rgmodel = RegressionModel.objects.get(Stock_code=stock_code, Date= test.loc[row_idx, 'date'])
		rgmodel.Predicted_data = test.loc[row_idx, 'predicted_data']
		rgmodel.save()


	ds1 = DataPool(
	   series=
		[{
			'options': {
				'source': RegressionModel.objects.all()
			},
			'terms': [
				'Date', 
				'Close', 'Predicted_data'
			]
		}])

	cht1 = Chart(
			datasource = ds1, 
			series_options = 
			[
				{'options':{
				  'type': 'line',
	              #'xAxis': 0,
	              #'yAxis': 0,
	              'zIndex': 1},
				'terms':{
				  'Date': [
					'Close'
					]
				  }},
				{'options':{
				  'type': 'scatter',
	              #'xAxis': 0,
	              #'yAxis': 0,
	              'zIndex': 0},
				'terms':{
				  'Date': [
					'Predicted_data'
					]
				  }}
			],
			chart_options =	
			  {'title':	{
				   'text': '%s Price of New York Stock Market' %(stock_code)},
			   'xAxis':	{
					'title': {
					   'text': 'Date of	All	Opening	'}}},
			x_sortf_mapf_mts = None
		)
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,
				'stock_code': stock_code,
				'charts' : [cht1],
				'stockcodelst':stockcodelst,}
	return render(request, 'index.html', context)
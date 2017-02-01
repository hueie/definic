from django.shortcuts import render
from chartit import DataPool, Chart
from .classes.datascience.regression import Regression
from .models_datascience import	RegressionModel
from .forms_datascience import RegressionForm
import copy

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
	
	regression = Regression()
	stockcodelst = regression.selectAllStockCodeFromDB()
	stockcodetop = regression.selectTopStockCodeFromDB()
	stock_code = (list(stockcodetop)[0])['stock_code']
	print(stock_code)
	
	if request.method == 'GET':
		form = RegressionForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStockcode']
			if(pStockCode != ""):
				stock_code = pStockCode
	elif request.method == 'POST':
		pass
	
	print(stock_code)
	rsltlst = regression.selectYahooDataFromDB(stock_code)
	predictedrsltlst = regression.linearregression(copy.deepcopy(rsltlst))
	
	RegressionModel.objects.all().delete()
	if	RegressionModel.objects.count() == 0:
		for	row in rsltlst:
			RegressionModel.objects.create(
				Stock_code = row['stock_code'], 
				Date = row['date'], 
				Lst_reg_dt = row['lst_reg_dt'], 
				Open = row['open'], 
				High = row['high'], 
				Low = row['low'], 
				Close = row['close'], 
				Volume = row['volume'],
				Adj_Close = row['adj_close'],
				Predicted_data = 0
				)
	
	for	row in predictedrsltlst:
		rgmodel = RegressionModel.objects.get(Stock_code=stock_code,Date=row['date'])
		rgmodel.Predicted_data = row['predicted_data']
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
	              'xAxis': 0,
	              'yAxis': 0,
	              'zIndex': 1},
				'terms':{
				  'Date': [
					'Close'
					]
				  }},
				{'options':{
				  'type': 'scatter',
	              'xAxis': 0,
	              'yAxis': 0,
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
from django.shortcuts import render
from .lineargraph import LinearGraph
from .statistics_models import	LinearGraphModel
from .statistics_forms import LinearGraphForm

from chartit import DataPool, Chart

	
	
def	lineargraph(request):
	mainmenu = "statistics" ; submenu = "lineargraph"

	lineargraph = LinearGraph()
	stockcodelst = lineargraph.selectAllStockCodeFromDB()
	stockcodetop = lineargraph.selectTopStockCodeFromDB()
	stock_code = (list(stockcodetop)[0])['stock_code']
	print(stock_code)
	
	if request.method == 'GET':
		form = LinearGraphForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStockcode']
			if(pStockCode != ""):
				stock_code = pStockCode
	elif request.method == 'POST':
		pass
	
	print(stock_code)
	rsltlst = lineargraph.selectYahooDataFromDB(stock_code)
	LinearGraphModel.objects.all().delete()
	if	LinearGraphModel.objects.count() == 0:
		for	row in rsltlst:
			LinearGraphModel.objects.create(
				Stock_code = row['stock_code'], 
				Date = row['date'], 
				Lst_reg_dt = row['lst_reg_dt'], 
				Open = row['open'], 
				High = row['high'], 
				Low = row['low'], 
				Close = row['close'], 
				Volume = row['volume'],
				Adj_Close = row['adj_close']
				)

	ds1 = DataPool(
	   series=
		[{
			'options': {
				'source': LinearGraphModel.objects.all()
			},
			'terms': [
				'Date', 
				'Open', 'High', 'Low', 'Close', 'Adj_Close'
			]
		}])

	cht1 = Chart(
			datasource = ds1, 
			series_options = 
			  [{'options':{
				  'type': 'line',
				  'stacking': False},
				'terms':{
				  'Date': [
					'Open', 'High', 'Low', 'Close', 'Adj_Close'
					]
				  }}],
			chart_options =	
			  {'title':	{
				   'text': '%s Price of New York Stock Market' %(stock_code)},
			   'xAxis':	{
					'title': {
					   'text': 'Date of	All	Opening	'}}},
			x_sortf_mapf_mts = None
		)

	ds2 = DataPool(
	   series=
		[{
			'options': {
				'source': LinearGraphModel.objects.all()
			},
			'terms': [
				'Date',
				'Volume'
			]
		}])

	cht2	= Chart(
			datasource = ds2, 
			series_options = 
			  [{'options':{
				  'type': 'column', #not bar
				  'stacking': False},
				'terms':{
				  'Date': [
					'Volume'
					]
				  }}],
			chart_options =	
			  {'title':	{
				   'text': '%s Volume of New York Stock Market' %(stock_code)},
			   'xAxis':	{
					'title': {
					   'text': 'Date of	All	Opening	'}}},
			x_sortf_mapf_mts = None
		)
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'stock_code': stock_code,
				'charts' : [cht1, cht2],
				'stockcodelst':stockcodelst,}
	return render(request, 'index.html', context)
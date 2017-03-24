from django.shortcuts import render
from .lineargraph import LinearGraph
from .descriptive import Descriptive
from .statistics_models import	LinearGraphModel, DescriptiveModel
from .statistics_forms import LinearGraphForm, DescriptiveForm
from ..backstage.datawarehouse import DataWareHouse

from chartit import DataPool, Chart

import numpy as np
from scipy import stats

def	descriptive(request):
	mainmenu = "statistics" ; submenu = "descriptive"

	datawarehouse = DataWareHouse()
	codelist = datawarehouse.selectAllStockCodeFromDB()
	stock_code = codelist.loc[0, 'stock_code']


	if request.method == 'GET':
		form = DescriptiveForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStock_code']
			if(pStockCode != ""):
				stock_code = pStockCode
	elif request.method == 'POST':
		pass
	print(stock_code)
	data = datawarehouse.selectYahooDataFromDB(stock_code)
	
	nparr1 = np.array(data['close'])
	nparr2 = np.array(data['open'])
	
	descriptive = Descriptive()
	descriptive.calallstats(nparr1, nparr2)
	
	DescriptiveModel.objects.all().delete()
	if	DescriptiveModel.objects.count() == 0:
		DescriptiveModel.objects.create(
			stock_code = stock_code, 
			amean =	descriptive.amean,
			hmean = descriptive.hmean,
			gmean = descriptive.gmean,
			median = descriptive.median,
			mode = descriptive.mode,
			min = descriptive.min,
			max = descriptive.max,
			q1 = descriptive.q1,
			q2 = descriptive.q2,
			q3 = descriptive.q3,
			var = descriptive.var,
			std = descriptive.std,
			cov = descriptive.cov,
			corr = descriptive.corr,
			)
	
	
	pCodelist = np.array( codelist['stock_code'] )
	pDescriptiveModel = DescriptiveModel.objects.all()
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pCodelist': pCodelist, 'pStock_code' : stock_code,
				'pDescriptiveModel': pDescriptiveModel,}
	return render(request, 'index.html', context)


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
			pStockCode = form.cleaned_data['pStock_code']
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
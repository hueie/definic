from django.shortcuts import render
from .datascience_forms import RegressionForm, PreprocessorForm, NeuralnetworkForm
from .datascience_models import	RegressionModel, PreprocessorModel

from chartit import DataPool, Chart
from .regression import LinearRegressionModel
from .neuralnetwork import MLPClassifierModel

from .preprocessor import Preprocessor
from ..backstage.datawarehouse import DataWareHouse
import numpy as np
import pandas as pd

def	preprocessor(request):
	mainmenu = "datascience" ; submenu = "preprocessor"
	
	datawarehouse = DataWareHouse()
	codelist = datawarehouse.selectAllStockCodeFromDB()
	stock_code = codelist.loc[0, 'stock_code']
	
	
	split_ratio = 0.8
	if request.method == 'GET':
		form = PreprocessorForm(request.GET)
		if form.is_valid():
			pStock_Code = form.cleaned_data['pStock_code']
			pSplit_ratio = form.cleaned_data['pSplit_ratio']
			if(pStock_Code != ""):
				stock_code = pStock_Code
			if(pSplit_ratio != ""):
				split_ratio = pSplit_ratio	
	elif request.method == 'POST':
		pass
	
	data = datawarehouse.selectYahooDataFromDB(stock_code)
	preprocessor = Preprocessor()
	train, test = preprocessor.splitDataset(data, split_ratio)
	
	PreprocessorModel.objects.all().delete()
	if	PreprocessorModel.objects.count() == 0:
		PreprocessorModel.objects.create(
			stock_code = stock_code,
			train = train, 
			test = test, 
			split_ratio = split_ratio
			)
		
	pPreprocessorModel = PreprocessorModel.objects.get(stock_code = stock_code)
	
	pCodelist = np.array( codelist['stock_code'] )
	'''	
	tmp2 = [ [t] for t in tmp]
	fieldlist = ['stock_code']
	pCodelist = map((lambda x: dict(zip(fieldlist, x))), tmp2)
	print(pCodelist)
	for row in pCodelist:
		print(row)
	'''
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pCodelist' : pCodelist, 
				'pPreprocessorModel' : pPreprocessorModel}
	return render(request, 'index.html', context)

def	regression(request):
	mainmenu = "datascience" ; submenu = "regression"

	datawarehouse = DataWareHouse()
	codelist = datawarehouse.selectAllStockCodeFromDB()
	stock_code = codelist.loc[0, 'stock_code']
	
	if request.method == 'GET':
		form = RegressionForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStock_code']
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
	
	pCodelist = np.array( codelist['stock_code'] )
	pRegressionModel = RegressionModel.objects.all()
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pCodelist':pCodelist, 'pStock_code':stock_code,
				'charts' : [cht1],
				'pRegressionModel':pRegressionModel,
				}
	return render(request, 'index.html', context)

def	neuralnetwork(request):
	mainmenu = "datascience" ; submenu = "neuralnetwork"

	datawarehouse = DataWareHouse()
	codelist = datawarehouse.selectAllStockCodeFromDB()
	stock_code = codelist.loc[0, 'stock_code']
	
	if request.method == 'GET':
		form = NeuralnetworkForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStock_code']
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

	mlpclassifiermodel = MLPClassifierModel()
	fit = mlpclassifiermodel.train( x_train, y_train)
	y_pred = mlpclassifiermodel.predict( x_test)
	score = mlpclassifiermodel.score(x_test, y_test)
	hitratio = mlpclassifiermodel.hitRatio(y_test, y_pred)
	mse = mlpclassifiermodel.meanSquaredError(y_test, y_pred)
	nodeshape = [mynode.shape for mynode in mlpclassifiermodel.model.coefs_] 
	test['predicted_data'] = pd.DataFrame(data=y_pred, index=test.index)
	
	
	pCodelist = np.array( codelist['stock_code'] )
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pCodelist':pCodelist, 'pStock_code':stock_code,
				'train' : train, 'test' : test, 'fit': fit, 
				'score': score, 'hitratio':hitratio,
				'mse' : mse, 'nodeshape':nodeshape
				}
	return render(request, 'index.html', context)

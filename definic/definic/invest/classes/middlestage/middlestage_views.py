from django.shortcuts import render
from .middlestage_models import	AlphaModelModel

from chartit import DataPool, Chart
from .alphamodel import MeanReversionModel, MachineLearningModel
from ..datascience.preprocessor import Preprocessor
from ..backstage.datawarehouse import DataWareHouse
import numpy as np
import pandas as pd

def	alphamodel(request):
	mainmenu = "middlestage" ; submenu = "alphamodel"

	datawarehouse = DataWareHouse()
	stock_code = "GOOG"
	data = datawarehouse.selectYahooDataFromDB(stock_code)
	preprocessor = Preprocessor()
	train, test = preprocessor.splitDataset(data, 0.9)

	x_train = np.array([ [row] for row in train['open'] ])
	y_train = np.array(train['adj_close'])

	x_test = np.array([ [row] for row in test['open'] ])
	y_test = np.array(test['adj_close'])

	alphamodel = MeanReversionModel()
	halflife = alphamodel.calcHalfLife(y_train)
	hurstexponent = alphamodel.calcHurstExponent(y_train, 4)
	adf = alphamodel.calcADF(y_train)
	mr_det_pos = alphamodel.determinePosition(x_train, y_train, x_test )

	alphamodel2 = MachineLearningModel()
	ml_det_pos = alphamodel2.determinePosition(x_train, y_train, x_test) 
	
	AlphaModelModel.objects.all().delete()
	if	AlphaModelModel.objects.count() == 0:
		AlphaModelModel.objects.create(
			stock_code = stock_code, 
			halflife = halflife, 
			hurstexponent = hurstexponent, 
			adf = adf,
			mr_det_pos = mr_det_pos,
			ml_det_pos = ml_det_pos
			)
	
	pAlphaModelModel = AlphaModelModel.objects.all()
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pAlphaModelModel': pAlphaModelModel,}
	return render(request, 'index.html', context)
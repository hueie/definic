from django.shortcuts import render
from .frontstage_models import	PortfolioBuilderModel

from chartit import DataPool, Chart
from .portfoliobuilder import PortfolioBuilder
from ..datascience.preprocessor import Preprocessor
from ..backstage.datawarehouse import DataWareHouse
import numpy as np
import pandas as pd

def	portfoliobuilder(request):
	mainmenu = "frontstage" ; submenu = "portfoliobuilder"


	datawarehouse = DataWareHouse()
	codelist = ["GOOG"]
	
	PortfolioBuilderModel.objects.all().delete()
	if	PortfolioBuilderModel.objects.count() == 0:
		data = datawarehouse.selectAllYahooDataFromDB()
		#preprocessor = Preprocessor()
		#train, test = preprocessor.splitDataset(data, 0.9)
		#PortFolio Builder logic will be changed 
		portfoliobuilder = PortfolioBuilder()
		df_stationarity = portfoliobuilder.doStationarityTest(data, codelist, 'close', 5)    
		df_rank = portfoliobuilder.rankStationarity(df_stationarity)
		stationarity_codes = portfoliobuilder.buildUniverse(df_rank,'rank',0.8)
		print(stationarity_codes)
		
		df_machine_result = portfoliobuilder.doMachineLearningTest(data, codelist, 'close', split_ratio=0.75,lags_count=5 )
		df_machine_rank = portfoliobuilder.rankMachineLearning(df_machine_result)
		machine_codes = portfoliobuilder.buildUniverse(df_machine_rank,'rank',0.8)
		print(machine_codes)
			
		PortfolioBuilderModel.objects.create(
			df_stationarity = df_stationarity, 
			df_rank = df_rank, 
			stationarity_codes = stationarity_codes,
			df_machine_result = df_machine_result,
			df_machine_rank = df_machine_rank,
			machine_codes = machine_codes
			)
	
	pPortfolioBuilderModel = PortfolioBuilderModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pPortfolioBuilderModel': pPortfolioBuilderModel,}
	return render(request, 'index.html', context)
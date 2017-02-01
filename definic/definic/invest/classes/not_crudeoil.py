"""
* Predicting Oil Gas By	using Logistic Regression.
Parameters
==========
data : dataframe
 Date :	2014-04-03	
 Open :	569.852553	
 High :	587.282679	
 Low : 564.132581  
 Close : 569.742571	 
 Volume	: 5099100
 Adj Close : 543.142460		  
 Log_Ret : -0.047813  
 Volatility	: 0.047813
 
stockratio : float
	Oil	stock ratio

productratio : float
	Oil	Production Rate

Returns
=======
expect : dataframe
 fprice	: float
	future price
 fstock	: float
	future stock

	, stockdata, stockratio, productratio
"""
import numpy as	np
import pandas as pd
import pandas.io.data as webdata

class Crudeoil:
	def	__init__(self, pdata=None):
		if pdata is	None:
			pdata =	webdata.DataReader('GOOG', data_source='yahoo',	start='4/3/2014', end='4/14/2014')
		self.data =	pdata

	def	predict( self ):
		print(self.data['Close'])
		return self.data

	def	analysis( self ):
		self.data['Log_Ret'] = np.log(self.data['Close'] / self.data['Close'].shift(1))
		self.data['Log_Ret'][0]	= 0
		self.data['Volatility']	= pd.rolling_std(self.data['Log_Ret'], window=2) * np.sqrt(2)
		self.data['Volatility'][0] = 0
		return self.data
	
	def	getObjSrc(self):	
		self.data['Date'] = self.data.index.values
		datalist = self.data.to_dict('list')
		return datalist
#-*- coding: utf-8 -*-
from datetime import datetime,timedelta
import os,math,pickle
import time
import numpy

class CommonUtil():
	def __init__(self):
		pass
	
	def getQuote(self, pstr):
		return "'%s'" % (pstr)
	
	def getDate(self):
		return time.strftime("%Y-%m-%d")
	
	def getTime(self):
		return time.strftime("%H:%M:%S")
	
	def clearString(self, value):
		new_value = value.replace("'",'`')
		new_value = new_value.replace('"',"'")	
		return new_value
	
	def last_day(self, d, day_name):
		days_of_week = ['sunday','monday','tuesday','wednesday', 'thursday','friday','saturday']
		target_day = days_of_week.index(day_name.lower())
		delta_day = target_day - d.isoweekday()
		if delta_day >= 0: 
			delta_day -= 7 # go back 7 days
		return d + timedelta(days=delta_day)
	
	def trim(self, value):
		words = ['\n','\r',' ','&nbsp;']
		new_str = str(value)
		for word in words:
			new_str = new_str.replace(word, '')
		return new_str
	
	def findBetween(self, s, first, last ):
		return (s.split(first))[1].split(last)[0]
	
	def findBetweenExt(self, s, first, last ):
		try:
			start = s.index( first ) + len( first )
			end = s.index( last, start )
			return s[start:end]
		except ValueError:
			return ""
	
	def getValue(self, pstr):
		new_str = self.trim(pstr)
		return self.clearString(new_str)
	
	
	def getNumericValue(self, pstr):
		new_str = self.trim(pstr)
		new_str = new_str.replace('"',"'")
		if new_str == "":
			return "0"
		return new_str
	
	def getSafeNumericValue(self, value):
		try:
				
			if value is None:
				return "0"
	
			if value=="":
				return "0"
				
			if math.isnan(float(value)):
				return "0"
			
			return str(value)
		except:
			print("Fatal Error!!! : getSafeNumericValue = %s" % (value))
			return "0"
	
	
	def convertMarketType(self, pstr):
		if pstr=='kospiVal':
			return 1
		elif pstr=='kosdaqVal':
			return 2
		return -1
	
	
	def convertStringToDate(self, value):
		value_year = value[0:4]
		value_month = value[4:6]
		value_day = value[6:8]
		#print "convertStringToDate : %s, %s, %s" % (value_year,value_month,value_day)
		return datetime(int(value_year), int(value_month), int(value_day)).strftime('%Y-%m-%d %H:%M:%S')
	
	
	def getDateByPerent(self, start_date,end_date,percent):
		days = (end_date - start_date).days
		target_days = numpy.trunc(days * percent)
		target_date = start_date + timedelta(days=target_days)
		print(days, target_days,target_date)
		return target_date
	
	
	def getPercentileIndex(self, percentile_arr,value):
		for index in range(len(percentile_arr)):
			if value<=percentile_arr[index]:
				return index
	
		return len(self, percentile_arr)
	
	
	def get_data_file_path(self, file_name):
		full_file_name = "%s/data/%s" % (os.path.dirname(os.path.abspath(__file__)),file_name)
		return full_file_name
	
	def saveToFile(self, filename):
		new_file_name = self.get_data_file_path(filename)
		pickle.dump(open( new_file_name, "wb" ))
	
	
	def loadFromFile(self, filename):
		new_file_name = self.get_data_file_path(filename)
		return pickle.load(open( new_file_name, "rb" ))

from django.db import models

class RegressionModel(models.Model):
	Stock_code = models.CharField(max_length=100)
	Date =	models.CharField(max_length=100) #TimeField
	Lst_reg_dt =	models.CharField(max_length=100) #TimeField
	Open = models.FloatField()
	High = models.FloatField()
	Low	= models.FloatField()
	Close =	models.FloatField()
	Volume = models.FloatField()
	Adj_Close =	models.FloatField()
	Predicted_data = models.FloatField(default=0)
	
	#DB Column End
	#Log_Ret	= models.FloatField()
	#Volatility = models.FloatField()

	def	save(self, *args, **kwargs):
		if self.Date ==	"":
			return
		else:
			super(RegressionModel, self).save(*args, **kwargs) # Call	the	"real" save() 
	

class PreprocessorModel(models.Model):
	stock_code = models.CharField(max_length=100, default="")
	train = models.CharField(max_length=100, default="")
	test =	models.CharField(max_length=100, default="") 
	split_ratio =	models.FloatField(max_length=100, default=0.0) 
	
	def	save(self, *args, **kwargs):
		super(PreprocessorModel, self).save(*args, **kwargs) 



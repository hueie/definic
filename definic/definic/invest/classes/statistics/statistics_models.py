from django.db import models

class DescriptiveModel(models.Model):
	stock_code = models.CharField(max_length=100)
	amean =	models.FloatField()
	hmean = models.FloatField()
	gmean = models.FloatField()
	median =	models.FloatField()
	mode	= models.CharField(max_length=100)
	min =	models.FloatField()
	max =	models.FloatField()
	q1 =	models.FloatField()
	q2 =	models.FloatField()
	q3 = models.FloatField()
	var =	models.FloatField()
	std =	models.FloatField()
	cov =	models.CharField(max_length=100)
	corr =	models.FloatField()

	def	save(self, *args, **kwargs):
		if self.stock_code ==	"":
			return
		else:
			super(DescriptiveModel, self).save(*args, **kwargs) # Call	the	"real" save() 
	

class LinearGraphModel(models.Model):
	Stock_code = models.CharField(max_length=100)
	Date =	models.CharField(max_length=100) #TimeField
	Lst_reg_dt =	models.CharField(max_length=100) #TimeField
	Open = models.FloatField()
	High = models.FloatField()
	Low	= models.FloatField()
	Close =	models.FloatField()
	Volume = models.FloatField()
	Adj_Close =	models.FloatField()
	#DB Column End
	#Log_Ret	= models.FloatField()
	#Volatility = models.FloatField()

	def	save(self, *args, **kwargs):
		if self.Date ==	"":
			return
		else:
			super(LinearGraphModel, self).save(*args, **kwargs) # Call	the	"real" save() 
	

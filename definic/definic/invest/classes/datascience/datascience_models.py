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
	

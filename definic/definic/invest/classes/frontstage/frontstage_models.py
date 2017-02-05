from django.db import models

class PortfolioBuilderModel(models.Model):
	
	df_stationarity =	models.CharField(max_length=100)
	df_rank =	models.CharField(max_length=100) #
	stationarity_codes =	models.CharField(max_length=100) #
	df_machine_result =	models.CharField(max_length=100) #
	df_machine_rank =	models.CharField(max_length=100) #
	machine_codes =	models.CharField(max_length=100) #

	def	save(self, *args, **kwargs):
		super(PortfolioBuilderModel, self).save(*args, **kwargs) # Call	the	"real" save() 
	

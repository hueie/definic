from django.db import models

class AlphaModelModel(models.Model):
	stock_code =	models.CharField(max_length=100)
	
	mr_det_pos =	models.CharField(max_length=100) #
	halflife =	models.CharField(max_length=100) #
	hurstexponent =	models.CharField(max_length=100) #
	adf =	models.CharField(max_length=100) #
	
	ml_det_pos =	models.CharField(max_length=100) #

	def	save(self, *args, **kwargs):
		if self.stock_code ==	"":
			return
		else:
			super(AlphaModelModel, self).save(*args, **kwargs) # Call	the	"real" save() 
	

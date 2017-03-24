from django.db import models

class DataWareHouseModel(models.Model):
	Stock_code = models.CharField(max_length=100)
	Start =	models.CharField(max_length=100) #TimeField
	End =	models.CharField(max_length=100) #TimeField
	Lst_reg_dt =	models.CharField(max_length=100) #TimeField

	def	save(self, *args, **kwargs):
		if self.Stock_code ==	"":
			return
		else:
			super(DataWareHouseModel, self).save(*args, **kwargs) # Call	the	"real" save() 
	

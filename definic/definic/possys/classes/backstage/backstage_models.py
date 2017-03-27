from django.db import models

class DataWareHouseModel(models.Model):
	In_out = models.CharField(max_length=100)
	From_to =	models.CharField(max_length=100) 
	Item_id =	models.CharField(max_length=100) 
	Expense =	models.CharField(max_length=100) 
	Quantity =	models.CharField(max_length=100) 
	Date =	models.CharField(max_length=100) 
	

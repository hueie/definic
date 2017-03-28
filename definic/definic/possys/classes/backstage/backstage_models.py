from django.db import models

class DataWareHouseModel(models.Model):
	In_out = models.CharField(max_length=100)
	From_to =	models.CharField(max_length=100) 
	Item_id =	models.CharField(max_length=100) 
	Expense =	models.CharField(max_length=100) 
	Quantity =	models.CharField(max_length=100) 
	Date =	models.CharField(max_length=100) 
	

class TransactionModel(models.Model):
	Tr_id = models.CharField(max_length=100)
	Pos_num =	models.CharField(max_length=100) 
	Item_id =	models.CharField(max_length=100) 
	Tr_price =	models.CharField(max_length=100) 
	Tr_quantity =	models.CharField(max_length=100) 
	Tr_date =	models.CharField(max_length=100) 
	

class ItemModel(models.Model):
	Item_id = models.CharField(max_length=100)
	Item_name =	models.CharField(max_length=100) 
	Barcode =	models.CharField(max_length=100) 
	Cur_price =	models.CharField(max_length=100) 
	Cur_quantity =	models.CharField(max_length=100) 
	Cur_place =	models.CharField(max_length=100) 
	Item_date =	models.CharField(max_length=100) 
	

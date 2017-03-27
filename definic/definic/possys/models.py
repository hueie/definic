from django.db import models

'''
class test1Model(models.Model):
	usrname_text = models.CharField(max_length=200)

class MonthlyWeatherByCity(models.Model):
	month =	models.IntegerField()
	boston_temp	= models.DecimalField(max_digits=5,	decimal_places=1)
	houston_temp = models.DecimalField(max_digits=5, decimal_places=1)

class CrudeOilModel(models.Model):
	Date =	models.DateField() #TimeField
	Open = models.FloatField()
	High = models.FloatField()
	Low	= models.FloatField()
	Close =	models.FloatField()
	Adj_Close =	models.FloatField()
	Volume = models.FloatField()
	Log_Ret	= models.FloatField()
	Volatility = models.FloatField()

	def	save(self, *args, **kwargs):
		if self.Date ==	"":
			return
		else:
			super(CrudeOilModel, self).save(*args, **kwargs) # Call	the	"real" save() 
'''	

	#def delete(self, *args, **kwargs):
	#	 if	self.name == "Yoko Ono's blog":
	#		 return	# Yoko shall never have	her	own	blog!
	#	 else:
	#		 super(CrudeOilModel, self).delete(*args, **kwargs)


	#def save_db_field(name,field,value):
	#	obj = MyModel.objects.get(name=name)
	#	obj.field = value
	#	obj.save()

	#def update_db_field(name,field,value):
	#	MyModel.objects.get(name=name).update(field=value)
from django.shortcuts import render
from .datawarehouse import DataWareHouse
from .backstage_forms import insertInventoryToDBForm
from .backstage_models import DataWareHouseModel

def	datawarehouse(request):
	mainmenu = "backstage" ; submenu = "datawarehouse"
	
	datawarehouse = DataWareHouse()
	rsltlst = datawarehouse.selectInventoryFromDB()
	print(rsltlst)
	DataWareHouseModel.objects.all().delete()
	if DataWareHouseModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			DataWareHouseModel.objects.create(
				In_out= rsltlst.loc[row_idx, 'in_out'],
				From_to= rsltlst.loc[row_idx, 'from_to'],
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Expense= rsltlst.loc[row_idx, 'expense'],
				Quantity= rsltlst.loc[row_idx, 'quantity'],
				Date= rsltlst.loc[row_idx, 'date']
				)
		
	pDataWareHouseModel = DataWareHouseModel.objects.all()
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pDataWareHouseModel': pDataWareHouseModel,}
	return render(request, 'index.html', context)

def	insertInventoryToDB(request):
	mainmenu = "backstage" ; submenu = "datawarehouse"
	pIn_out = "" ; pFrom_to = "" ; pItem_id = ""
	pExpense = "" ; pQuantity = "" ; pDate = ""
	datawarehouse = DataWareHouse()
					
	if request.method == 'GET':
		form = insertInventoryToDBForm(request.GET)
		if form.is_valid():
			pIn_out = form.cleaned_data['pIn_out']
			pFrom_to = form.cleaned_data['pFrom_to']
			pItem_id = form.cleaned_data['pItem_id']
			pExpense = form.cleaned_data['pExpense']
			pQuantity = form.cleaned_data['pQuantity']
			pDate = form.cleaned_data['pDate']
			
			datawarehouse.insertInventoryToDB(pIn_out, pFrom_to, pItem_id, pExpense, pQuantity, pDate)

	elif request.method == 'POST':
		pass
	
	
	
	rsltlst = datawarehouse.selectInventoryFromDB()
	
	DataWareHouseModel.objects.all().delete()
	if DataWareHouseModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			DataWareHouseModel.objects.create(
				In_out= rsltlst.loc[row_idx, 'in_out'],
				From_to= rsltlst.loc[row_idx, 'from_to'],
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Expense= rsltlst.loc[row_idx, 'expense'],
				Quantity= rsltlst.loc[row_idx, 'quantity'],
				Date= rsltlst.loc[row_idx, 'date']
				)
		
	pDataWareHouseModel = DataWareHouseModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pIn_out':pIn_out,'pFrom_to':pFrom_to,'pItem_id':pItem_id,
				'pExpense':pExpense,'pQuantity':pQuantity,'pDate':pDate,
				'pDataWareHouseModel': pDataWareHouseModel}
	return render(request, 'index.html', context)

from django.shortcuts import render
from .inventory import Inventory
from .transaction import Transaction
from .item import Item
from .itemcategory import Itemcategory
from .backstage_forms import insertInventoryToDBForm, insertTransactionToDBForm, insertItemToDBForm
from .backstage_models import InventoryModel, TransactionModel, ItemModel, ItemcategoryModel


def	inventory(request):
	mainmenu = "backstage" ; submenu = "inventory"
	
	inventory = Inventory()
	rsltlst = inventory.selectInventoryFromDB()

	InventoryModel.objects.all().delete()
	if InventoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			InventoryModel.objects.create(
				Inv_id= rsltlst.loc[row_idx, 'inv_id'],
				In_out= rsltlst.loc[row_idx, 'in_out'],
				From_to= rsltlst.loc[row_idx, 'from_to'],
				Inv_item_id= rsltlst.loc[row_idx, 'inv_item_id'],
				Inv_expense= rsltlst.loc[row_idx, 'inv_expense'],
				Inv_quantity= rsltlst.loc[row_idx, 'inv_quantity'],
				Inv_date= rsltlst.loc[row_idx, 'inv_date']
				)
		
	pInventoryModel = InventoryModel.objects.all()
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pInventoryModel': pInventoryModel,}
	return render(request, 'possys/index.html', context)

def	insertInventoryToDB(request):
	mainmenu = "backstage" ; submenu = "inventory"
	pIn_out = "" ; pFrom_to = "" ; pItem_id = ""
	pExpense = "" ; pQuantity = "" ; pDate = ""
	inventory = Inventory()
					
	if request.method == 'GET':
		form = insertInventoryToDBForm(request.GET)
		if form.is_valid():
			pInv_id = form.cleaned_data['pInv_id']
			pIn_out = form.cleaned_data['pIn_out']
			pFrom_to = form.cleaned_data['pFrom_to']
			pInv_item_id = form.cleaned_data['pInv_item_id']
			pInv_expense = form.cleaned_data['pInv_expense']
			pInv_quantity = form.cleaned_data['pInv_quantity']
			pInv_date = form.cleaned_data['pInv_date']
			
			maxInv_id = inventory.selectMaxInv_idFromDB()
			if maxInv_id.loc[0,'MAX(inv_id)'] == None:
				maxInv_id_p_1=0
			else:
				maxInv_id_p_1 = maxInv_id.loc[0,'MAX(inv_id)']
			maxInv_id_p_1 = int(maxInv_id_p_1) + 1
			inventory.insertInventoryToDB(maxInv_id_p_1, pIn_out, pFrom_to, pInv_item_id, pInv_expense, pInv_quantity, pInv_date)

	elif request.method == 'POST':
		pass
	else:
		pass
	rsltlst = inventory.selectInventoryFromDB()
	
	InventoryModel.objects.all().delete()
	if InventoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			InventoryModel.objects.create(
				Inv_id= rsltlst.loc[row_idx, 'inv_id'],
				In_out= rsltlst.loc[row_idx, 'in_out'],
				From_to= rsltlst.loc[row_idx, 'from_to'],
				Inv_item_id= rsltlst.loc[row_idx, 'inv_item_id'],
				Inv_expense= rsltlst.loc[row_idx, 'inv_expense'],
				Inv_quantity= rsltlst.loc[row_idx, 'inv_quantity'],
				Inv_date= rsltlst.loc[row_idx, 'inv_date']
				)
		
	pInventoryModel = InventoryModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pIn_out':pIn_out,'pFrom_to':pFrom_to,'pItem_id':pItem_id,
				'pExpense':pExpense,'pQuantity':pQuantity,'pDate':pDate,
				'pInventoryModel': pInventoryModel}
	return render(request, 'possys/index.html', context)


def	item(request):
	mainmenu = "backstage" ; submenu = "item"
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()

	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	
	
	item = Item()
	rsltlst = item.selectItemFromDB()

	ItemModel.objects.all().delete()
	if ItemModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemModel.objects.create(
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Item_name= rsltlst.loc[row_idx, 'item_name'],
				Barcode= rsltlst.loc[row_idx, 'barcode'],
				Cur_price= rsltlst.loc[row_idx, 'cur_price'],
				Cur_quantity= rsltlst.loc[row_idx, 'cur_quantity'],
				Cur_place= rsltlst.loc[row_idx, 'cur_place'],
				Item_date= rsltlst.loc[row_idx, 'item_date'],
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id']
				)
		
	pItemModel = ItemModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemModel': pItemModel,'pItemcategoryModel':pItemcategoryModel,}
	return render(request, 'possys/index.html', context)

def	insertItemToDB(request):
	mainmenu = "backstage" ; submenu = "item"
	pItem_id = "" ; pItem_name = "" ; pBarcode = ""
	pCur_price = "" ; pCur_quantity = "" ; pCur_place = "" ; pItem_date = "" ; pItemcategory_id = ""
	item = Item()
					
	if request.method == 'GET':
		form = insertItemToDBForm(request.GET)
		if form.is_valid():
			pItem_id = form.cleaned_data['pItem_id']
			pItem_name = form.cleaned_data['pItem_name']
			pBarcode = form.cleaned_data['pBarcode']
			pCur_price = form.cleaned_data['pCur_price']
			pCur_quantity = form.cleaned_data['pCur_quantity']
			pCur_place = form.cleaned_data['pCur_place']
			pItem_date = form.cleaned_data['pItem_date'],
			pItemcategory_id = form.cleaned_data['pItemcategory_id']
			
			maxItem_id = item.selectMaxItem_idFromDB()
			if maxItem_id.loc[0,'MAX(item_id)'] == None:
				maxItem_id_p_1 = 0;
			else:
				maxItem_id_p_1 = maxItem_id.loc[0,'MAX(item_id)']
			maxItem_id_p_1 = int(maxItem_id_p_1) + 1
			item.insertItemToDB(maxItem_id_p_1, pItem_name, pBarcode, pCur_price, pCur_quantity, pCur_place, pItem_date, pItemcategory_id)

	elif request.method == 'POST':
		pass
	else:
		pass
	rsltlst = item.selectItemFromDB()
	
	ItemModel.objects.all().delete()
	if ItemModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemModel.objects.create(
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Item_name= rsltlst.loc[row_idx, 'item_name'],
				Barcode= rsltlst.loc[row_idx, 'barcode'],
				Cur_price= rsltlst.loc[row_idx, 'cur_price'],
				Cur_quantity= rsltlst.loc[row_idx, 'cur_quantity'],
				Cur_place= rsltlst.loc[row_idx, 'cur_place'],
				Item_date= rsltlst.loc[row_idx, 'item_date'],
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id']
				)
		
	pItemModel = ItemModel.objects.all()
	
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()

	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItem_id':pItem_id,'pItem_name':pItem_name,'pBarcode':pBarcode,
				'pCur_price':pCur_price,'pCur_quantity':pCur_quantity,'pCur_place':pCur_place,'pItem_date':pItem_date,'pItemcategory_id':pItemcategory_id,
				'pItemModel': pItemModel, 'pItemcategoryModel':pItemcategoryModel,}
	return render(request, 'possys/index.html', context)


def	updateItemToDB(request):
	mainmenu = "backstage" ; submenu = "item"
	pItem_id = "" ; pItem_name = "" ; pBarcode = ""
	pCur_price = "" ; pCur_quantity = "" ; pCur_place = "" ; pItem_date = ""; pItemcategory_id = "" 
	item = Item()
					
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pItem_id = request.POST.get('pItem_id')
		pItem_name = request.POST.get('pItem_name')
		pBarcode = request.POST.get('pBarcode')
		pCur_price = request.POST.get('pCur_price')
		pCur_quantity = request.POST.get('pCur_quantity')
		pCur_place = request.POST.get('pCur_place')
		pItem_date = request.POST.get('pItem_date')
		pItemcategory_id = request.POST.get('pItemcategory_id')
		item.updateItemToDB(pItem_id, pItem_name, pBarcode, pCur_price, pCur_quantity, pCur_place, pItem_date,pItemcategory_id)
		pass
	else:
		pass
	rsltlst = item.selectItemFromDB()
	
	ItemModel.objects.all().delete()
	if ItemModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemModel.objects.create(
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Item_name= rsltlst.loc[row_idx, 'item_name'],
				Barcode= rsltlst.loc[row_idx, 'barcode'],
				Cur_price= rsltlst.loc[row_idx, 'cur_price'],
				Cur_quantity= rsltlst.loc[row_idx, 'cur_quantity'],
				Cur_place= rsltlst.loc[row_idx, 'cur_place'],
				Item_date= rsltlst.loc[row_idx, 'item_date'],
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id']
				)
		
	pItemModel = ItemModel.objects.all()
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()

	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItem_id':pItem_id,'pItem_name':pItem_name,'pBarcode':pBarcode,
				'pCur_price':pCur_price,'pCur_quantity':pCur_quantity,'pCur_place':pCur_place,'pItem_date':pItem_date,'pItemcategory_id':pItemcategory_id,
				'pItemModel': pItemModel,'pItemcategoryModel':pItemcategoryModel}
	return render(request, 'possys/index.html', context)


def	deleteItemToDB(request):
	mainmenu = "backstage" ; submenu = "item"
	pItem_id = "" ; pItem_name = "" ; pBarcode = ""
	pCur_price = "" ; pCur_quantity = "" ; pCur_place = "" ; pItem_date = "" ; pItemcategory_id = ""
	item = Item()
					
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pItem_id = request.POST.get('pItem_id')
		item.deleteItemToDB(pItem_id)
		pass
	else:
		pass
	
	rsltlst = item.selectItemFromDB()
	
	ItemModel.objects.all().delete()
	if ItemModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemModel.objects.create(
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Item_name= rsltlst.loc[row_idx, 'item_name'],
				Barcode= rsltlst.loc[row_idx, 'barcode'],
				Cur_price= rsltlst.loc[row_idx, 'cur_price'],
				Cur_quantity= rsltlst.loc[row_idx, 'cur_quantity'],
				Cur_place= rsltlst.loc[row_idx, 'cur_place'],
				Item_date= rsltlst.loc[row_idx, 'item_date'],
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				)
		
	pItemModel = ItemModel.objects.all()
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()

	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItem_id':pItem_id,'pItem_name':pItem_name,'pBarcode':pBarcode,
				'pCur_price':pCur_price,'pCur_quantity':pCur_quantity,'pCur_place':pCur_place,'pItem_date':pItem_date,'pItemcategory_id':pItemcategory_id,
				'pItemModel': pItemModel,'pItemcategoryModel':pItemcategoryModel,}
	return render(request, 'possys/index.html', context)



def	transaction(request):
	mainmenu = "backstage" ; submenu = "transaction"
	
	transaction = Transaction()
	rsltlst = transaction.selectTransactionFromDB()

	TransactionModel.objects.all().delete()
	if TransactionModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			TransactionModel.objects.create(
				Tr_id= rsltlst.loc[row_idx, 'tr_id'],
				Pos_num= rsltlst.loc[row_idx, 'pos_num'],
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Tr_price= rsltlst.loc[row_idx, 'tr_price'],
				Tr_quantity= rsltlst.loc[row_idx, 'tr_quantity'],
				Tr_date= rsltlst.loc[row_idx, 'tr_date']
				)
		
	pTransactionModel = TransactionModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pTransactionModel': pTransactionModel,}
	return render(request, 'possys/index.html', context)

def	insertTransactionToDB(request):
	mainmenu = "backstage" ; submenu = "transaction"
	transaction = Transaction()
					
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pTr_id = request.POST.get('pTr_id')
		pPos_num = request.POST.get('pPos_num') if request.POST.get('pPos_num') != "" else 0
		pItem_idlist = request.POST.getlist('pItem_id')
		pTr_pricelist = request.POST.getlist('pTr_price')
		pTr_quantitylist = request.POST.getlist('pTr_quantity')
		pTr_Date = request.POST.get('pTr_Date')
		
		maxTransaction_id = transaction.selectMaxTransaction_idFromDB()
		if maxTransaction_id.loc[0,'MAX(tr_id)'] == None:
			maxTransaction_id_p_1 = 0
		else:
			maxTransaction_id_p_1 = maxTransaction_id.loc[0,'MAX(tr_id)']
		maxTransaction_id_p_1 = int(maxTransaction_id_p_1) + 1
		print(maxTransaction_id_p_1)
		for idx in range(len(pItem_idlist)):
			if(pItem_idlist[idx] != ""):
				transaction.insertTransactionToDB(maxTransaction_id_p_1, pPos_num, pItem_idlist[idx], pTr_pricelist[idx], pTr_quantitylist[idx], pTr_Date)
		pass
	else:
		pass
	
	rsltlst = transaction.selectTransactionFromDB()
	
	TransactionModel.objects.all().delete()
	if TransactionModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			TransactionModel.objects.create(
				Tr_id= rsltlst.loc[row_idx, 'tr_id'],
				Pos_num= rsltlst.loc[row_idx, 'pos_num'],
				Item_id= rsltlst.loc[row_idx, 'item_id'],
				Tr_price= rsltlst.loc[row_idx, 'tr_price'],
				Tr_quantity= rsltlst.loc[row_idx, 'tr_quantity'],
				Tr_date= rsltlst.loc[row_idx, 'tr_date']
				)
		
	pTransactionModel = TransactionModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pTransactionModel': pTransactionModel}
	return render(request, 'possys/index.html', context)






def	itemcategory(request):
	mainmenu = "backstage" ; submenu = "itemcategory"
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()

	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemcategoryModel': pItemcategoryModel,}
	return render(request, 'possys/index.html', context)

def	insertItemcategoryToDB(request):
	mainmenu = "backstage" ; submenu = "itemcategory"
	pItemcategory_id = "" ; pItemcategory_name = "" ; pItemcategory_content = ""; pItemcategory_date = ""
	itemcategory = Itemcategory()
					
	if request.method == 'GET':
		pass	
	elif request.method == 'POST':
		pItemcategory_id = request.POST.get('pItemcategory_id')
		pItemcategory_name = request.POST.get('pItemcategory_name')
		pItemcategory_content = request.POST.get('pItemcategory_content')
		pItemcategory_date = request.POST.get('pItemcategory_date')
		
		maxItemcategory_id = itemcategory.selectMaxItemcategory_idFromDB()
		if maxItemcategory_id.loc[0,'max_itemcategory_id'] == None:
			maxItemcategory_id_p_1 = 0;
		else:
			maxItemcategory_id_p_1 = maxItemcategory_id.loc[0,'max_itemcategory_id']
		maxItemcategory_id_p_1 = int(maxItemcategory_id_p_1) + 1
		itemcategory.insertItemcategoryToDB(maxItemcategory_id_p_1, pItemcategory_name, pItemcategory_content, pItemcategory_date)
		pass
	else:
		pass
	rsltlst = itemcategory.selectItemcategoryFromDB()
	
	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemcategory_id':pItemcategory_id,'pItemcategory_name':pItemcategory_name,'pItemcategory_content':pItemcategory_content,'pItemcategory_date':pItemcategory_date,
				'pItemcategoryModel': pItemcategoryModel}
	return render(request, 'possys/index.html', context)


def	updateItemcategoryToDB(request):
	mainmenu = "backstage" ; submenu = "itemcategory"
	pItemcategory_id = "" ; pItemcategory_name = "" ; pItemcategory_content = "" ; pItemcategory_date = ""
	itemcategory = Itemcategory()
					
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pItemcategory_id = request.POST.get('pItemcategory_id')
		pItemcategory_name = request.POST.get('pItemcategory_name')
		pItemcategory_content = request.POST.get('pItemcategory_content')
		pItemcategory_date = request.POST.get('pItemcategory_date')
		itemcategory.updateItemcategoryToDB(pItemcategory_id, pItemcategory_name, pItemcategory_content, pItemcategory_date)
		pass
	else:
		pass
	rsltlst = itemcategory.selectItemcategoryFromDB()
	
	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemcategory_id':pItemcategory_id,'pItemcategory_name':pItemcategory_name,'pItemcategory_content':pItemcategory_content, 'pItemcategory_date':pItemcategory_date,
				'pItemcategoryModel': pItemcategoryModel}
	return render(request, 'possys/index.html', context)


def	deleteItemcategoryToDB(request):
	mainmenu = "backstage" ; submenu = "itemcategory"
	pItemcategory_id = "" ; pItemcategory_name = "" ; pItemcategory_content = "" ; pItemcategory_date = ""
	itemcategory = Itemcategory()
					
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pItemcategory_id = request.POST.get('pItemcategory_id')
		itemcategory.deleteItemcategoryToDB(pItemcategory_id)
		pass
	else:
		pass
	
	rsltlst = itemcategory.selectItemcategoryFromDB()
	
	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_content'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemcategory_id':pItemcategory_id,'pItemcategory_name':pItemcategory_name,'pItemcategory_content':pItemcategory_content, 'pItemcategory_date':pItemcategory_date,
				'pItemcategoryModel': pItemcategoryModel}
	return render(request, 'possys/index.html', context)



def	posdatamart(request):
	mainmenu = "backstage" ; submenu = "posdatamart"
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,}
	return render(request, 'possys/index.html', context)


def	uploadposdata(request):
	mainmenu = "backstage" ; submenu = "posdatamart"
	from django.core.files.storage import FileSystemStorage
	
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		pass
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'uploaded_file_url': uploaded_file_url
				}
	return render(request, 'possys/index.html', context)



'''
Django multiple input field values with same name

{% for question in questions %}
    <input type="hidden" name="question" value="{{ question.id }}/>

    {% for answer in question.get_answers %}
        <input type="radio" name="answer-{{ question.id }}" value={{ answer.score }}>
    {% endfor %}
{% endfor %}
views.py

questions = request.POST.getlist('question')
answers = [request.POST['answer-{}'.format(q)] for q in questions]
'''
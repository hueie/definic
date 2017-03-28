from django.shortcuts import render
from .datawarehouse import DataWareHouse
from .transaction import Transaction
from .item import Item
from .backstage_forms import insertInventoryToDBForm, insertTransactionToDBForm, insertItemToDBForm
from .backstage_models import DataWareHouseModel, TransactionModel, ItemModel

def	datawarehouse(request):
	mainmenu = "backstage" ; submenu = "datawarehouse"
	
	datawarehouse = DataWareHouse()
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
	else:
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


def	item(request):
	mainmenu = "backstage" ; submenu = "item"
	
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
				Item_date= rsltlst.loc[row_idx, 'item_date']
				)
		
	pItemModel = ItemModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemModel': pItemModel,}
	return render(request, 'index.html', context)

def	insertItemToDB(request):
	mainmenu = "backstage" ; submenu = "item"
	pItem_id = "" ; pItem_name = "" ; pBarcode = ""
	pCur_price = "" ; pCur_quantity = "" ; pCur_place = "" ; pItem_date = ""
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
			pItem_date = form.cleaned_data['pItem_date']
			
			maxItem_id = item.selectMaxItem_idFromDB()
			maxItem_id_p_1 = int(maxItem_id.loc[0,'MAX(item_id)']) + 1
			item.insertItemToDB(maxItem_id_p_1, pItem_name, pBarcode, pCur_price, pCur_quantity, pCur_place, pItem_date)

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
				Item_date= rsltlst.loc[row_idx, 'item_date']
				)
		
	pItemModel = ItemModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItem_id':pItem_id,'pItem_name':pItem_name,'pBarcode':pBarcode,
				'pCur_price':pCur_price,'pCur_quantity':pCur_quantity,'pCur_place':pCur_place,'pItem_date':pItem_date,
				'pItemModel': pItemModel}
	return render(request, 'index.html', context)


def	updateItemToDB(request):
	mainmenu = "backstage" ; submenu = "item"
	pItem_id = "" ; pItem_name = "" ; pBarcode = ""
	pCur_price = "" ; pCur_quantity = "" ; pCur_place = "" ; pItem_date = ""
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
		item.updateItemToDB(pItem_id, pItem_name, pBarcode, pCur_price, pCur_quantity, pCur_place, pItem_date)
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
				Item_date= rsltlst.loc[row_idx, 'item_date']
				)
		
	pItemModel = ItemModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItem_id':pItem_id,'pItem_name':pItem_name,'pBarcode':pBarcode,
				'pCur_price':pCur_price,'pCur_quantity':pCur_quantity,'pCur_place':pCur_place,'pItem_date':pItem_date,
				'pItemModel': pItemModel}
	return render(request, 'index.html', context)


def	deleteItemToDB(request):
	mainmenu = "backstage" ; submenu = "item"
	pItem_id = "" ; pItem_name = "" ; pBarcode = ""
	pCur_price = "" ; pCur_quantity = "" ; pCur_place = "" ; pItem_date = ""
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
				Item_date= rsltlst.loc[row_idx, 'item_date']
				)
		
	pItemModel = ItemModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItem_id':pItem_id,'pItem_name':pItem_name,'pBarcode':pBarcode,
				'pCur_price':pCur_price,'pCur_quantity':pCur_quantity,'pCur_place':pCur_place,'pItem_date':pItem_date,
				'pItemModel': pItemModel}
	return render(request, 'index.html', context)



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
	return render(request, 'index.html', context)

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
		maxTransaction_id_p_1 = int(maxTransaction_id.loc[0,'MAX(tr_id)']) + 1
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
	return render(request, 'index.html', context)



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
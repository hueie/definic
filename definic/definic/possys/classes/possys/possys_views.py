from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from ..backstage.item import Item
from ..backstage.itemcategory import Itemcategory
from ..backstage.backstage_models import ItemModel, ItemcategoryModel

def	index(request):
	mainmenu = "possys" ; submenu = "index"
	
	if request.method == 'GET':
		first_itemcategory_id=""
		pass
	elif request.method == 'POST':
		first_itemcategory_id = request.POST.get('selected_itemcategory_id')
		pass
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()
	if first_itemcategory_id == "":
		first_itemcategory_id = rsltlst.loc[0, 'itemcategory_id'];
	
	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
		
	pItemcategoryCnt = ItemcategoryModel.objects.count();	
	pItemcategoryModel = ItemcategoryModel.objects.all()
	
	item = Item()
	rsltlst = item.selectItemFromDB(first_itemcategory_id)

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
		
	pItemCnt = ItemModel.objects.count();	
	pItemModel = ItemModel.objects.all()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemCnt':pItemCnt, 'pItemcategoryCnt': pItemcategoryCnt,
				'pItemModel': pItemModel,'pItemcategoryModel': pItemcategoryModel,}
	return render(request, 'index.html', context)


def	selectItemcategory(request):
	mainmenu = "possys" ; submenu = "index"
	
	if request.method == 'GET':
		first_itemcategory_id=""
		pass
	elif request.method == 'POST':
		first_itemcategory_id = request.POST.get('selected_itemcategory_id')
		pass
	
	itemcategory = Itemcategory()
	rsltlst = itemcategory.selectItemcategoryFromDB()
	if first_itemcategory_id == "":
		first_itemcategory_id = rsltlst.loc[0, 'itemcategory_id'];
	
	ItemcategoryModel.objects.all().delete()
	if ItemcategoryModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			ItemcategoryModel.objects.create(
				Itemcategory_id= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_name= rsltlst.loc[row_idx, 'itemcategory_name'],
				Itemcategory_content= rsltlst.loc[row_idx, 'itemcategory_id'],
				Itemcategory_date= rsltlst.loc[row_idx, 'itemcategory_date']
				)
	
	pItemcategoryCnt = ItemcategoryModel.objects.count();	
	pItemcategoryModel = serializers.serialize('json', ItemcategoryModel.objects.all())  
	
	item = Item()
	rsltlst = item.selectItemFromDB(first_itemcategory_id)

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
		
	pItemCnt = ItemModel.objects.count();	
	pItemModel = serializers.serialize('json', ItemModel.objects.all()) 
	
	
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'pItemCnt':pItemCnt, 'pItemcategoryCnt': pItemcategoryCnt,
				'pItemModel': pItemModel,'pItemcategoryModel': pItemcategoryModel,}
	return JsonResponse(context)





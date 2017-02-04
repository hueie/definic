from django.shortcuts import render
from .datawarehouse import DataWareHouse
from .backstage_forms import DataUpdateForm
from .backstage_models import DataWareHouseModel

def	datawarehouse(request):
	mainmenu = "backstage" ; submenu = "datawarehouse"
	maintitle="backstage" ; subtitle="datawarehouse"
	
	datawarehouse = DataWareHouse()
	rsltlst = datawarehouse.selectYahooPeriodDataFromDB()
	
	DataWareHouseModel.objects.all().delete()
	if DataWareHouseModel.objects.count() == 0:
		for row_idx in range(rsltlst.shape[0]):
			DataWareHouseModel.objects.create(
				Stock_code= rsltlst.loc[row_idx, 'stock_code'],
				Start= rsltlst.loc[row_idx, 'start'],
				End= rsltlst.loc[row_idx, 'end'],
				Lst_reg_dt= rsltlst.loc[row_idx, 'lst_reg_dt']
				)
		
	pDataWareHouseModel = DataWareHouseModel.objects.all()
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,
				'pDataWareHouseModel': pDataWareHouseModel,}
	return render(request, 'index.html', context)

def	dataUpdate(request):
	mainmenu = "backstage" ; submenu = "datawarehouse"
	maintitle="backstage" ; subtitle="datawarehouse"
	pStockCode = "" ; pStart = "" ; pEnd = ""
	datawarehouse = DataWareHouse()
					
	if request.method == 'GET':
		form = DataUpdateForm(request.GET)
		if form.is_valid():
			pStockCode = form.cleaned_data['pStockcode']
			pStart = form.cleaned_data['pStart']
			pEnd = form.cleaned_data['pEnd']
			#print(pStockCode);print(pStart);print(pEnd)
			
			datawarehouse.getYahooDataFromWeb(pStockCode, pStart, pEnd)
			datawarehouse.updateYahooData()

	elif request.method == 'POST':
		pass
	
	rsltlst = datawarehouse.selectYahooDataFromDB()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,
				'pStockCode':pStockCode,'pStart':pStart,'pEnd':pEnd,
				'rsltlst':rsltlst,
				}
	return render(request, 'index.html', context)

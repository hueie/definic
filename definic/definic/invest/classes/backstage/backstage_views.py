from django.shortcuts import render
from .classes.backstage.datawarehouse import DataWareHouse
from .forms_backstage import DataUpdateForm

def	datawarehouse(request):
	mainmenu = "backstage" ; submenu = "datawarehouse"
	maintitle="backstage" ; subtitle="datawarehouse"
	
	datawarehouse = DataWareHouse()
	rsltlst = datawarehouse.selectYahooDataFromDB()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,
				'rsltlst': rsltlst,}
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

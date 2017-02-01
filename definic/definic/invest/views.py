from django.shortcuts import render

def	index(request):
	mainmenu = "datascience"
	submenu = "machinelearning"
	maintitle="datascience"
	subtitle="machinelearning"
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,}
	
	return render(request, 'index.html', context)





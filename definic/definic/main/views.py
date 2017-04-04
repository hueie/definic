from django.shortcuts import render
def	index(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"
	
	print("main")
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,}
	
	
	return render(request, 'main/index.html', context)





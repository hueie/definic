from django.shortcuts import render
from .classes.common.dbhandler import DBHandler

def	index(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"
	
	dbhandler = DBHandler()
	dbhandler.initdb()
	
	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,}
	
	
	return render(request, 'possys/index.html', context)





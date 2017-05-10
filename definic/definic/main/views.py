from django.shortcuts import render
from .classes.commonmain.dbhandler import DBHandler
from .classes.login.login import Login

def	index(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"

	dbhandler = DBHandler()
	dbhandler.initdb()

	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,}
	return render(request, 'main/index.html', context)


def login(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"
	msg=""
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		user_pwd = request.POST.get('user_pwd')
		
		#Check Logic
		
		login = Login()
		rsltlst = login.selectLoginData(user_id, user_pwd)
		print(len(rsltlst))
		print(rsltlst['cnt'][0])
		if rsltlst['cnt'][0] != 0:
			request.session['user_id'] = user_id
			msg="Welcome"
		else:
			msg="Access Denied"
		pass
	else:
		pass   
	context = {'mainmenu': mainmenu, 'submenu': submenu, 'maintitle': maintitle, 'subtitle': subtitle,'msg':msg,}
	return render(request, 'main/index.html', context)

def logout(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"
	try:
		del request.session['user_id']
	except:
		pass
	context = {'mainmenu': mainmenu, 'submenu': submenu, 'maintitle': maintitle, 'subtitle': subtitle,}
	return render(request, 'main/index.html', context)



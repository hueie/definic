from django.shortcuts import render
def	index(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"

	context	= {'mainmenu': mainmenu, 'submenu': submenu,
				'maintitle': maintitle, 'subtitle': subtitle,}
	return render(request, 'main/index.html', context)


def login(request):
	mainmenu = "index"
	submenu = "index"
	maintitle="index"
	subtitle="index"
	
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		user_pwd = request.POST.get('user_pwd')
		#Check Logic
		request.session['user_id'] = user_id
		pass
	else:
		pass   
	context = {'mainmenu': mainmenu, 'submenu': submenu, 'maintitle': maintitle, 'subtitle': subtitle,}
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



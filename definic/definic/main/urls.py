from django.conf.urls import url
from . import views

urlpatterns	= [
	url(r'^$', views.index,	name='main_index'), 
	url(r'^login/$', views.login,	name='main_login'), 
	url(r'^logout/$', views.logout,	name='main_logout'), 
	
	
]
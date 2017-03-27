from django.conf.urls import url
from . import views
from .classes.backstage import backstage_views


urlpatterns	= [
	url(r'^$', views.index,	name='index'), 
	url(r'^backstage/datawarehouse/$', backstage_views.datawarehouse,	name='datawarehouse'), 
	url(r'^backstage/datawarehouse/update/$', backstage_views.dataUpdate,	name='dataUpdate'), 
	
#	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='alphamodel'), 
	
#	url(r'^frontstage/portfoliobuilder/$', frontstage_views.portfoliobuilder,	name='portfoliobuilder'), 
	
]
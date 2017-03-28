from django.conf.urls import url
from . import views
from .classes.backstage import backstage_views


urlpatterns	= [
	url(r'^$', views.index,	name='index'), 
	url(r'^backstage/datawarehouse/$', backstage_views.datawarehouse,	name='datawarehouse'), 
	url(r'^backstage/datawarehouse/insertInventoryToDB/$', backstage_views.insertInventoryToDB,	name='insertInventoryToDB'), 
	
	url(r'^backstage/transaction/$', backstage_views.transaction,	name='transaction'), 
	url(r'^backstage/transaction/insertTransactionToDB/$', backstage_views.insertTransactionToDB,	name='insertTransactionToDB'), 
	
	url(r'^backstage/item/$', backstage_views.item,	name='item'), 
	url(r'^backstage/item/insertItemToDB/$', backstage_views.insertItemToDB,	name='insertItemToDB'), 
	url(r'^backstage/item/deleteItemToDB/$', backstage_views.deleteItemToDB,	name='deleteItemToDB'), 
	url(r'^backstage/item/updateItemToDB/$', backstage_views.updateItemToDB,	name='updateItemToDB'), 
	
#	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='alphamodel'), 
	
#	url(r'^frontstage/portfoliobuilder/$', frontstage_views.portfoliobuilder,	name='portfoliobuilder'), 
	
]
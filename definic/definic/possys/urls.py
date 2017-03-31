from django.conf.urls import url
from . import views
from .classes.backstage import backstage_views
from .classes.possys import possys_views


urlpatterns	= [
	url(r'^$', possys_views.index,	name='index'), 
	url(r'^selectItemcategory/$', possys_views.selectItemcategory,	name='selectItemcategory'), 

	url(r'^backstage/inventory/$', backstage_views.inventory,	name='inventory'), 
	url(r'^backstage/inventory/insertInventoryToDB/$', backstage_views.insertInventoryToDB,	name='insertInventoryToDB'), 
	
	url(r'^backstage/transaction/$', backstage_views.transaction,	name='transaction'), 
	url(r'^backstage/transaction/insertTransactionToDB/$', backstage_views.insertTransactionToDB,	name='insertTransactionToDB'), 
	
	url(r'^backstage/item/$', backstage_views.item,	name='item'), 
	url(r'^backstage/item/insertItemToDB/$', backstage_views.insertItemToDB,	name='insertItemToDB'), 
	url(r'^backstage/item/deleteItemToDB/$', backstage_views.deleteItemToDB,	name='deleteItemToDB'), 
	url(r'^backstage/item/updateItemToDB/$', backstage_views.updateItemToDB,	name='updateItemToDB'), 
	
	url(r'^backstage/itemcategory/$', backstage_views.itemcategory,	name='itemcategory'), 
	url(r'^backstage/itemcategory/insertItemcategoryToDB/$', backstage_views.insertItemcategoryToDB,	name='insertItemcategoryToDB'), 
	url(r'^backstage/itemcategory/deleteItemcategoryToDB/$', backstage_views.deleteItemcategoryToDB,	name='deleteItemcategoryToDB'), 
	url(r'^backstage/itemcategory/updateItemcategoryToDB/$', backstage_views.updateItemcategoryToDB,	name='updateItemcategoryToDB'), 
#	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='alphamodel'), 
	
#	url(r'^frontstage/portfoliobuilder/$', frontstage_views.portfoliobuilder,	name='portfoliobuilder'), 
	
]
from django.conf.urls import url
from . import views
from .classes.backstage import backstage_views
from .classes.possys import possys_views


urlpatterns	= [
	url(r'^$', possys_views.index,	name='possys_index'), 
	url(r'^selectItemcategory/$', possys_views.selectItemcategory,	name='possys_selectItemcategory'), 

	url(r'^backstage/inventory/$', backstage_views.inventory,	name='possys_inventory'), 
	url(r'^backstage/inventory/insertInventoryToDB/$', backstage_views.insertInventoryToDB,	name='possys_insertInventoryToDB'), 
	
	url(r'^backstage/transaction/$', backstage_views.transaction,	name='possys_transaction'), 
	url(r'^backstage/transaction/insertTransactionToDB/$', backstage_views.insertTransactionToDB,	name='possys_insertTransactionToDB'), 
	
	url(r'^backstage/item/$', backstage_views.item,	name='possys_item'), 
	url(r'^backstage/item/insertItemToDB/$', backstage_views.insertItemToDB,	name='possys_insertItemToDB'), 
	url(r'^backstage/item/deleteItemToDB/$', backstage_views.deleteItemToDB,	name='possys_deleteItemToDB'), 
	url(r'^backstage/item/updateItemToDB/$', backstage_views.updateItemToDB,	name='possys_updateItemToDB'), 
	
	url(r'^backstage/itemcategory/$', backstage_views.itemcategory,	name='possys_itemcategory'), 
	url(r'^backstage/itemcategory/insertItemcategoryToDB/$', backstage_views.insertItemcategoryToDB,	name='possys_insertItemcategoryToDB'), 
	url(r'^backstage/itemcategory/deleteItemcategoryToDB/$', backstage_views.deleteItemcategoryToDB,	name='possys_deleteItemcategoryToDB'), 
	url(r'^backstage/itemcategory/updateItemcategoryToDB/$', backstage_views.updateItemcategoryToDB,	name='possys_updateItemcategoryToDB'), 
#	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='alphamodel'), 
	
#	url(r'^frontstage/portfoliobuilder/$', frontstage_views.portfoliobuilder,	name='portfoliobuilder'), 
	
]
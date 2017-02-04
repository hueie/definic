from django.conf.urls import url
from . import views
from .classes.statistics import statistics_views
from .classes.datascience import datascience_views
from .classes.backstage import backstage_views
from .classes.middlestage import middlestage_views


urlpatterns	= [
	url(r'^$', views.index,	name='index'), 
	url(r'^statistics/lineargraph/$', statistics_views.lineargraph,	name='lineargraph'), 
	
	url(r'^datascience/machinelearning/$', datascience_views.machinelearning,	name='machinelearning'), 
	url(r'^datascience/regression/$', datascience_views.regression,	name='regression'), 
	
	url(r'^backstage/datawarehouse/$', backstage_views.datawarehouse,	name='datawarehouse'), 
	url(r'^backstage/datawarehouse/update/$', backstage_views.dataUpdate,	name='dataUpdate'), 
	
	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='alphamodel'), 
	
]
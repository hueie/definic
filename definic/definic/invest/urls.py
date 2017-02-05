from django.conf.urls import url
from . import views
from .classes.statistics import statistics_views
from .classes.datascience import datascience_views
from .classes.backstage import backstage_views
from .classes.middlestage import middlestage_views
from .classes.frontstage import frontstage_views


urlpatterns	= [
	url(r'^$', views.index,	name='index'), 
	url(r'^statistics/lineargraph/$', statistics_views.lineargraph,	name='lineargraph'), 
	
	url(r'^datascience/regression/$', datascience_views.regression,	name='regression'), 
	url(r'^datascience/preprocessor/$', datascience_views.preprocessor,	name='preprocessor'), 
	
	url(r'^backstage/datawarehouse/$', backstage_views.datawarehouse,	name='datawarehouse'), 
	url(r'^backstage/datawarehouse/update/$', backstage_views.dataUpdate,	name='dataUpdate'), 
	
	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='alphamodel'), 
	
	url(r'^frontstage/portfoliobuilder/$', frontstage_views.portfoliobuilder,	name='portfoliobuilder'), 
	
]
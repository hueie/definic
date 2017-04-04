from django.conf.urls import url
from . import views
from .classes.statistics import statistics_views
from .classes.datascience import datascience_views
from .classes.backstage import backstage_views
from .classes.middlestage import middlestage_views
from .classes.frontstage import frontstage_views


urlpatterns	= [
	url(r'^$', views.index,	name='invest_index'), 
	url(r'^statistics/descriptive/$', statistics_views.descriptive,	name='invest_descriptive'), 
	url(r'^statistics/lineargraph/$', statistics_views.lineargraph,	name='invest_lineargraph'), 
	
	url(r'^datascience/regression/$', datascience_views.regression,	name='invest_regression'), 
	url(r'^datascience/neuralnetwork/$', datascience_views.neuralnetwork,	name='invest_neuralnetwork'), 
	url(r'^datascience/preprocessor/$', datascience_views.preprocessor,	name='invest_preprocessor'), 
	
	url(r'^backstage/datawarehouse/$', backstage_views.datawarehouse,	name='invest_datawarehouse'), 
	url(r'^backstage/datawarehouse/update/$', backstage_views.dataUpdate,	name='invest_dataUpdate'), 
	
	url(r'^middlestage/alphamodel/$', middlestage_views.alphamodel,	name='invest_alphamodel'), 
	
	url(r'^frontstage/portfoliobuilder/$', frontstage_views.portfoliobuilder,	name='invest_portfoliobuilder'), 
	
]
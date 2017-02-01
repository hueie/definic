from django.conf.urls import url
from . import views
from . import views_statistics
from . import views_datascience
from . import views_backstage


urlpatterns	= [
	url(r'^$', views.index,	name='index'), 
	url(r'^statistics/lineargraph/$', views_statistics.lineargraph,	name='lineargraph'), 
	
	url(r'^datascience/machinelearning/$', views_datascience.machinelearning,	name='machinelearning'), 
	url(r'^datascience/regression/$', views_datascience.regression,	name='regression'), 
	
	url(r'^backstage/datawarehouse/$', views_backstage.datawarehouse,	name='datawarehouse'), 
	url(r'^backstage/datawarehouse/update/$', views_backstage.dataUpdate,	name='dataUpdate'), 
	
]
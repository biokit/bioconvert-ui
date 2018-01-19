# Create your views here.
from django.conf.urls import url

# Routers provide an easy way of automatically determining the URL conf.
from bioconvertapi.views import BioconvertView, BioconvertConversionView
from bioconvertwebui import views

app_name = 'bioconvertwebui'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^conversion/(?P<identifier>[0-9A-Za-z]{32,32})/$', views.results, name='results'),
]

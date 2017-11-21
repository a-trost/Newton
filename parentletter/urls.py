from django.conf.urls import url

from . import views

app_name = 'parentletter'

urlpatterns = [
     url(r'(?i)print/(?P<arg>[a-z0-9\-]+)/$', views.parent_letters, name='parentletters'),
     # url(r'(?i)print/(?P<classroom>[a-z0-9\-]+)/$', views.class_roster, name='printclass'),

]
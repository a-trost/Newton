from django.conf.urls import url
from django.urls import reverse

from . import views

app_name = 'ixl'

urlpatterns = [
    url(r'(?i)lists/?$', views.ixl_lists, name='ixl_lists'),
    url(r'(?i)lists/view/?$', views.view_lists, name='ixl_view_lists'),
    url(r'(?i)lists/create$', views.ixl_list_create, name='ixl_list_create'),
    url(r'(?i)lists/view/(?P<list>[a-z0-9]+)', views.view_single_list, name='ixl_view_single_list'),
    url(r'(?i)lists/edit/exercises/(?P<list>[a-z0-9]+)$', views.ixl_list_exercise_assign,
        name='ixl_assign_list_exercises'),
    url(r'(?i)lists/edit/(?P<list>[a-z0-9]+)$', views.edit_list, name='ixl_edit_list'),
    url(r'(?i)lists/delete/(?P<list>[a-z0-9]+)$', views.delete_list, name='ixl_delete_list'),
    url(r'(?i)lists/edit/(?P<list>[a-z0-9]+)/students$', views.ixl_assign_list, name='ixl_assign_list'),

    # assign_list_to_students
    # ixl_list_exercise_assign
    # /skill/A-B.2
    # url(r'(?i)skill/(?P<skill_id>\w-\w\.\d+)$', views.skill_detail, name='skilldetail'),
    # /level/D
    # url(r'(?i)level/(?P<level>\w)$', views.level_detail, name='leveldetail'),
    # /16-17/2nd/Trost
    # url(r'^(?i)/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/?$', views.class_list, name='classlist'),

]
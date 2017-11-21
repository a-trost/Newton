from django.conf.urls import url
from django.core.urlresolvers import reverse

from . import views

app_name = 'brain'

urlpatterns = [
    # /16-17/2nd/trost/   Class List
    url(r'^(?i)portal/toolkit/timer/?$', views.timer, name='timer'),
    url(r'^(?i)portal/toolkit/pledge/?$', views.pledge, name='pledge'),
    url(r'^(?i)portal/toolkit/music/?$', views.music, name='music'),
    url(r'^(?i)portal/attendance/?$', views.attendance_teacher_list, name='attendance'),
    url(r'^(?i)portal/attendance/chronic/?$', views.attendance_chronic_student_list, name='attendancechronic'),

    url(r'^(?i)portal/attendance/(?P<classroom_last_name>[a-z0-9\-]+)/?$', views.attendance_class_detail, name='attendanceclass'),

    url(r'^(?i)class/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/?$', views.class_list, name='classlist'),
    # /student/83   Student Detail
    url(r'^(?i)student/(?P<studentid>[0-9]+)/?$', views.student_detail, name='studentdetail'),
    url(r'^(?i)portal/morning/create?$', views.CreateMessage.as_view(template_name="brain/morningmessage_form.html",)),

    # Portal URLS
    url(r'^(?i)portal/?$', views.portal_school, name='portalschool'),
    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/?$', views.portal_class, name='portalclass'),
    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/pass/(?P<studentid>[0-9]+)/?$', views.password,
        name='password'),
    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/(?P<studentid>[0-9]+)/?$', views.portal_student, name='portalstudent'),
    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/groups/?$', views.make_groups, name='makegroups'),
    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/toolkit/?$', views.toolkit, name='toolkit'),

    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/morning/?$', views.morning_message, name='morningmessage'),
    url(r'^(?i)portal/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/random/?$', views.random_student,
        name='randomstudent'),

    url(r'^$', views.index, name='index'),]

from django.conf.urls import url

from . import views

app_name = 'scoreit'

urlpatterns = [
    # /log/45
     url(r'(?i)log/(?P<student_id>[a-z0-9\-]+)$', views.class_list, name='classlist'),
    url(r'(?i)log/(?P<student_id>[a-z0-9\-]+)/(?P<subject>[a-z0-9\s]+)$', views.log_subject, name='logsubject'),
    url(r'(?i)gradeview/$', views.grade_view, name='gradeview'),
    url(r'(?i)gradeview/yesterday$', views.grade_view_yesterday, name='gradeviewyesterday'),
    url(r'(?i)gradeview/twodays', views.grade_view_twodays, name='gradeviewtwodays'),
    url(r'(?i)gradeview/threedays', views.grade_view_threedays, name='gradeviewthreedays'),

    # # /level/D
    # url(r'(?i)/level/(?P<level>\w)$', views.level_detail, name='leveldetail'),
    # # /16-17/2nd/Trost

]
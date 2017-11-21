from django.conf.urls import url

from . import views

app_name = 'amc'

urlpatterns = [
    url(r'^(?i)(?P<grade>[a-z0-9]+)/printchallenge', views.print_challenge_sheets_grade,
        name='challengesheetsgrade'),
url(r'^(?i)(?P<grade>[a-z0-9]+)/printtest', views.print_test_sheets_grade,
        name='testsheetsgrade'),
    # /16-17/2nd/Trost/input
    url(r'^(?i)(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/input$',
        views.input_amc_scores, name='inputamcscores'),
    url(r'^(?i)(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/cba/(?P<test_type>[a-z0-9\-]+)',
        views.print_cba_test_sheets_class, name='cbasheetsclass'),
    # /16-17/2nd/Trost
    url(r'^(?i)(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/?$', views.class_list,
        name='classlist'),
    # /16-17
    url(r'^(?i)(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/printchallenge$',
        views.print_challenge_sheets_class,
        name='challengesheetsclass'),
    url(r'^(?i)(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/printtest$',
        views.print_test_sheets_class,
        name='testsheetsclass'),

    # url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/(?P<classroom>[a-z0-9\-]+)/addition',
    #     views.print_cba_test_sheets_class,
    #     name='cbasheetsclass'),

    # url(r'^(?i)(?P<year>[0-9]{2}-[0-9]{2})/(?P<grade>[a-z0-9]+)/print$', views.print_challenge_sheets_grade,
    #     name='challengesheetsgrade'),


    url(r'^$', views.school_roster, name='schoolroster'),
]

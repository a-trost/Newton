from django.conf.urls import  include, url
from django.contrib import admin

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # url('^', include('django.contrib.auth.urls')),
    url(r'^(?i)admin/', include(admin.site.urls), name='admin'),
url(r'^(?i)login/$', auth_views.login, {'template_name': 'brain/login.html',}, name='login'),
    url(r'^(?i)logout/$', auth_views.logout,{'template_name': 'brain/logout.html', 'next_page': '/'}, name='logout'),
url(r'^(?i)password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^(?i)password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^(?i)reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^(?i)reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^(?i)amc/', include('amc.urls')),
    url(r'^(?i)nwea/', include('nwea.urls')),
    # url(r'^(?i)classes/', include('brain.urls'), ),
    url(r'^(?i)ixl/', include('ixl.urls')),
    url(r'^(?i)cgi/', include('mathcgi.urls')),
    url(r'^(?i)scoreit/', include('scoreit.urls')),
    url(r'^(?i)parentletter/', include('parentletter.urls')),
    url(r'^(?i)stickers/', include('badges.urls')),
    # url(r'^(?i)eni/', include('eni.urls')),
    # url(r'^(?i)cba/', include('cba.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon/favicon.ico')),
    url(r'^', include('brain.urls'), ),

]

urlpatterns += staticfiles_urlpatterns()



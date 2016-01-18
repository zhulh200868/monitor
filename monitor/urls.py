from django.conf.urls import patterns, include, url
from django.contrib import admin
from web import views 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('web.urls')),
    (r'^graph/$', views.graph),
    url(r'^nagios/$', views.get_data),
    url(r'^gethostname/$', views.gethostname),
    url(r'^getservice_name/$', views.getservice_name),
)

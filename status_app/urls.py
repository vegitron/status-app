from django.conf.urls import patterns, url

urlpatterns = patterns('status_app.views',
    url(r'', 'status'),
)

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    "",
    url(r'^$', 'django_chat.views.chat'),
)

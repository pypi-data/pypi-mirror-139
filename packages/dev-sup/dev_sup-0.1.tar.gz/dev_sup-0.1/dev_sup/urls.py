from django.urls import path, re_path

from . import views

app_name = "dev_sup"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<slug>[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*)/$',
            views.site, name='site')
]

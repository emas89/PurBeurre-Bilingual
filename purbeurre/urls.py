from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<id_product>[0-9]+)/$', views.detail, name='detail'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.sign_up, name='sign_up'),
    url(r'^account/$', views.account, name='account'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^legals/$', views.legals, name='legals'),
    url(r'^saved/$', views.saved, name='saved')
]
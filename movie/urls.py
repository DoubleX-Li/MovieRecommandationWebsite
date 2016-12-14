from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name = 'index'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^logout/$',views.logout,name = 'logout'),
    url(r'^watched/$',views.WatchedView.as_view(),name = 'watched'),
    url(r'^recommand/$',views.RecommandView.as_view() ,name = 'recommand'),
    url(r'^browse/$', views.browse, name = 'browse'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name = 'detail'),
]
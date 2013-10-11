__author__ = 'chenglu'
from django.conf.urls import patterns, url

from nb_webapp import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       #url(r'^register/$', views.RegisterView.as_view(), name='Sign up'),
                       url(r'^register/$', views.register, name='Register'),
                       url(r'^hello', views.hello, name='hello'),
                       url(r'^home', views.home, name='home'),
                       url(r'^welcome', views.welcome, name='welcome'),
                       url(r'^login', views.nb_login, name='login'),
                       url(r'^page_signup', views.page_signup, name='page_signup'),
                       url(r'^signup', views.nb_signup, name='signup'),
)

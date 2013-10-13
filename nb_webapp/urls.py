__author__ = 'chenglu'
from django.conf.urls import patterns, url

from nb_webapp import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       #url(r'^register/$', views.RegisterView.as_view(), name='Sign up'),
                       url(r'^register/$', views.register, name='Register'),
                       url(r'^home', views.home, name='home'),
                       url(r'^welcome', views.welcome, name='welcome'),
                       url(r'^login', views.nb_login, name='login'),
                       url(r'^page_signup', views.page_signup, name='page_signup'),
                       url(r'^signup', views.nb_signup, name='signup'),
                       url(r'^logout', views.nb_logout, name='logout'),
                       url(r'^show_post', views.nb_show_post, name='show_post'),
                       url(r'^post_card', views.nb_post_card, name='post_card'),
                       url(r'^profile', views.nb_profile, name='profile'),
)

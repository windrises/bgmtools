"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from myapp import views as myapp_views

urlpatterns = [
    url(r'^$', myapp_views.home, name='home'),
    url(r'^bgmtools/$', myapp_views.bgmtools, name='bgmtools'),
    url(r'^bgmtools/contrast/(.*)', myapp_views.contrast, name='contrast'),
    url(r'^bgmtools/multitag/(.*)', myapp_views.multitag, name='multitag'),
    url(r'^bgmtools/review/chart($|/.*)', myapp_views.review_chart, name='review_chart'),
    url(r'^bgmtools/review/list($|/.*)', myapp_views.review_list, name='review_list'),
    url(r'^bgmtools/review($|/.*)', myapp_views.review_chart, name='review'),
    url(r'^admin/', include(admin.site.urls)),
]

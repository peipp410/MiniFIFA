"""football URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from football import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home_view, name='home'),
    re_path(r'^index$', views.home_view, name='home'),
    re_path(r'^information$', views.team_view, name='information'),
    re_path(r'^evaluation$', views.evaluation_view, name='evaluation'),
    re_path(r'^players/([0-9]+)$', views.players, name='players'),
    re_path(r'^management$', views.management_view, name='management'),
    re_path(r'^clubs/([\s\S]+)$', views.clubs, name='clubs'),
    re_path(r'^about$', views.about_view, name='about'),
    re_path(r'^tutorial$', views.tutorial_view, name='tutorial')
]

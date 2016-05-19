"""oneliner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    url('^logout', auth_views.logout, {'template_name': 'registration/logout.html'}),
    url('^', include('django.contrib.auth.urls')),

    # Front-end
    url(r'^$', views.home, name='home'),
    url(r'^register/?$', views.register, name='register'),

    # Dashboard
    url(r'^accounts/profile/?$', views.profile, name='profile'),
    url(r'^accounts/survey/?$', views.survey, name='survey'),

    # Services, add service
    url(r'^services/add/([\w\s]+)/?$', views.service_add, name='service_add'),
    url(r'^services/edit/([\w\s]+)/?$', views.service_edit, name='service_edit'),
    url(r'^services/remove/([\w\s]+)/?$', views.service_remove, name='service_remove'),
    url(r'^services/?$', views.services, name='services'),

    # *The* javascript view
    url(r'^js/(\d+)/app.js$', views.one_liner_js, name='one_liner_js'),

    # Instructions page
    url(r'^instructions/?$', views.instructions, name='instructions')
]

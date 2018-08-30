"""photogal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from photosite import views
from django.conf.urls import url, include


urlpatterns = [
	url(r'^accounts/login/$',views.LoginView, name='login'),
	url(r'^accounts/logout/$',views.LogoutView, name='logout'),
	url(r'^list/(?P<path>.+)/$', views.List, name='list'),		
	url(r'^thumb/(?P<path>.+)/$', views.Thumb, name='thumb'),		
	url(r'^$', views.List, name='list'),
	url(r'^fav/(?P<path>.+)/(?P<value>[1,0])/$', views.SetFav, name='setfav'),
	url(r'^favorites/$', views.PageFav, name='favpage'),
	url(r'^image/(?P<path>.+)/$', views.Preview, name='image'),			
    path('admin/', admin.site.urls),

]

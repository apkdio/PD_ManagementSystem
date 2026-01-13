"""
URL configuration for example01 project.

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app03.view import department, user, superman, login_out, consumer,logging

urlpatterns = [
    path('depart/list/', department.depart_list),
    path('depart/add/', department.depart_add),
    path('depart/<int:nid>/delete/', department.depart_delete),
    path('user/list/<int:nid>/', user.user_list),
    path('user/add/', user.user_add),
    path('user/<int:nid>/delete/', user.user_delete),
    path('depart/<int:nid>/edit/', department.depart_edit),
    path('user/<int:nid>/edit/', user.user_edit),
    path('main/', login_out.login),
    path('manager/', superman.superman),
    path('manager/add/', superman.superman_add),
    path('manager/reset/<int:nid>/', superman.reset_pass),
    path('manager/<int:nid>/edit/', superman.superman_edit),
    path('manager/<int:nid>/delete/', superman.superman_delete),
    path('code/img/', login_out.image_code, name="code"),
    path('logout/', login_out.logout),
    path('consumer/list/<int:nid>/', consumer.consumer_list),
    path('consumer/add/', consumer.consumer_add),
    path('consumer/<int:nid>/delete/', consumer.consumer_delete),
    path('consumer/<int:nid>/edit/', consumer.consumer_edit),
    path('depart/master/', department.master_set),
    path('depart/master/<int:nid>/', department.master_set),
    path('logging/<str:string>/<int:nid>/<str:name>', logging.log),
    path('admin/', admin.site.urls)
]

from django.urls import path

from home import views as home_views

from . import views

urlpatterns = [
    path("", home_views.home, name="home"),
    path("create/", views.create_account, name="create_account"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.campaigns, name="campaigns"),
    path("create/", views.create_campaign, name="create_campaign"),
    path("delete/<uuid:uuid>/", views.delete_campaign, name="delete_campaign"),
]

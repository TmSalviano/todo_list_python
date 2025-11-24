from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("all/", views.all_items, name="all"),
    path("<int:todoitem_id>/", views.detail, name="detail"),
    path("<int:todoitem_id>/delete/", views.delete, name="delete"),
]
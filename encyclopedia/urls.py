from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new-page/", views.new_page, name="new-page"),
    path("edit-page/<str:title>/", views.edit_page, name="edit-page")
]
from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("read/<int:book_id>/", views.read_book, name="read_book"),

]



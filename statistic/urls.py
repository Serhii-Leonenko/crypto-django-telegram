from django.urls import path

from statistic.views import index, favourites_change, favourites_list

urlpatterns = [
    path("", index, name="index"),
    path("<str:uuid>/favourites_change/", favourites_change, name="favourites_change"),
    path("favourites/", favourites_list, name="favourite_list")
]

app_name = "statistic"

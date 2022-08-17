from django.urls import path

from statistic.views import index, favourites_change, FavouriteListView

urlpatterns = [
    path("", index, name="index"),
    path("<int:pk>/favourites_change/", favourites_change, name="favourites_change"),
    path("favourites/", FavouriteListView.as_view(), name="favourite_list")
]

app_name = "statistic"

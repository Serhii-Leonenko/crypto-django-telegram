from django.urls import path

from statistic.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "statistic"

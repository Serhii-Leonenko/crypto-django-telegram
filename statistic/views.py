import os
from urllib.parse import urljoin
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic

import requests

from statistic.models import Coin


@login_required
def index(request):
    url = urljoin(os.getenv("PARSE_URL"), "coins")
    headers = {"x-access-token": os.getenv("API_KEY")}
    response = requests.get(url, headers=headers)
    data = response.json()["data"]["coins"]
    for coin in data:
        name = coin["name"]
        uuid = coin["uuid"]
        price = coin["price"]
        rank = coin["rank"]
        market_cap = f"{int(coin['marketCap']):,}"
        icon = coin["iconUrl"]
        symbol = coin["symbol"]

        obj, created = Coin.objects.update_or_create(
            name=name,
            symbol=symbol,
            uuid=uuid,
            icon=icon,
            defaults={
                "rank": rank,
                "price": price,
                "market_cap": market_cap
            }
        )

    context = {
        "coins": Coin.objects.all()
    }

    return render(request, "statistic/index.html", context=context)


class FavouriteListView(mixins.LoginRequiredMixin, generic.ListView):
    model = Coin
    template_name = "statistic/index.html"
    context_object_name = "coins"

    def get_queryset(self):
        return Coin.objects.filter(users__in=[self.request.user])


def favourites_change(request, pk):
    user = request.user
    coin = Coin.objects.get(pk=pk)
    if user in coin.users.all():
        coin.users.remove(user)
    else:
        coin.users.add(user)
    return redirect(request.META['HTTP_REFERER'])

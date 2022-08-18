import os
from urllib.parse import urljoin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import requests

from statistic.models import Coin


@login_required
def index(request):
    url = urljoin(os.getenv("PARSE_URL"), "coins")
    headers = {"x-access-token": os.getenv("API_KEY")}
    response = requests.get(url, headers=headers)
    coins = response.json()["data"]["coins"]
    favourite_coins_uuid = [
        coin.uuid
        for coin in Coin.objects.filter(users__in=[request.user])
    ]

    context = {
        "coins": coins,
        "favourites": favourite_coins_uuid
    }

    return render(request, "statistic/index.html", context=context)


@login_required
def favourites_list(request):
    favourites = Coin.objects.filter(users__in=[request.user])
    favourite_coins_uuid = []
    coins = []
    for favourite_coin in favourites:
        favourite_coins_uuid.append(favourite_coin.uuid)
        url = urljoin(os.getenv("PARSE_URL"), f"coin/{favourite_coin.uuid}")
        headers = {"x-access-token": os.getenv("API_KEY")}
        response = requests.get(url, headers=headers)
        coin = response.json()["data"]["coin"]
        coins.append({
            "rank": coin["rank"],
            "name": coin["name"],
            "symbol": coin["symbol"],
            "uuid": favourite_coin.uuid,
            "price": coin["price"],
            "iconUrl": coin["iconUrl"],
            "marketCa": coin["marketCap"]
        })

    context = {
        "coins": coins,
        "favourites": favourite_coins_uuid
    }

    return render(request, "statistic/index.html", context=context)


def favourites_change(request, uuid):
    user = request.user
    url = urljoin(os.getenv("PARSE_URL"), f"coin/{uuid}")
    headers = {"x-access-token": os.getenv("API_KEY")}
    response = requests.get(url, headers=headers)
    coin = response.json()["data"]["coin"]
    coin, _ = Coin.objects.get_or_create(
        rank=coin["rank"],
        name=coin["uuid"],
        symbol=coin["symbol"],
        uuid=coin["uuid"],
    )
    if user in coin.users.all():
        coin.users.remove(user)
    else:
        coin.users.add(user)
    return redirect(request.META['HTTP_REFERER'])

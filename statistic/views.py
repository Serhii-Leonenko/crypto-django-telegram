import datetime
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from app.settings import TIME_ZONE
from statistic.forms import DateForm


@login_required
def index(request):
    url = os.getenv("PARSE_URL")
    headers = {"Api-Key": os.getenv("API_KEY")}

    today = datetime.datetime.today()
    start_date = today.isoformat()
    end_date = today.isoformat()

    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"].isoformat()
            end_date = form.cleaned_data["end_date"].isoformat()
    else:
        form = DateForm()

    data = {
        "range": {
            "from": start_date,
            "to": end_date,
            "timezone": TIME_ZONE,
            "interval": "custom_date_range",
        },
        "metrics": ["clicks", "conversions"],
        "filters": [
            {"name": "sub_id_6",
             "operator": "CONTAINS",
             "expression": request.user.username}
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    content = response.json()["rows"][0]
    clicks = content["clicks"]
    conversions = content["conversions"]

    context = {
        "clicks": clicks,
        "conversions": conversions,
        "form": form,
    }

    return render(request, "statistic/index.html", context=context)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from datetime import  datetime, timezone
from herokuapp.models import *

# Create your views here.

API_KEY = 'JDPbPLEw7KcUi3bllJWzjGMmG'
API_KEY_SECRET = 'N4pYueGKKJGwzEdg0hLY7bnj3VeHqjasmNXtQH8tPJr83o7xfY'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAACC%2FhgEAAAAAk4ceasHvdrsDddeaDJYXtpyfaWI%3DShbR4sLzWDcvfLClsGPrQ6HfzqgeZoUIjbSLiyXxfxq2OtpM3K'


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def get_user_id(username):
    url = "https://api.twitter.com/2/users/by?usernames={}".format(username)

    response = requests.request("GET", url, auth=bearer_oauth, )
    print(response.status_code)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()['data'][0]['id']


def hey_view(request):
    username = request.GET.get('user')
    res = {'res':False}

    if State.objects.count() > 0 and (datetime.now(timezone.utc) - State.objects.all()[0].last_update).total_seconds() < 2*15*60:
        res['res'] = Suspects.objects.filter(username__exact=username).count() > 0
        if res['res']:
            s = Suspects.objects.get(username__exact=username)
            s.num_ask += 1
            s.save()
        return JsonResponse(res)

    s = State.objects.create(last_update=datetime.now(timezone.utc))
    s.save()

    username_main = 'asdfasd79743432'
    user_id_main = get_user_id(username_main)
    url = "https://api.twitter.com/2/users/{}/following".format(user_id_main)
    params = {"user.fields": "created_at"}
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    for user in Suspects.objects.all():
        user.delete()
    for user in response.json()['data']:
        s = Suspects.objects.create(username=user['username'], num_ask=0)
        if username == user['username']:
            res['res'] = True
            s.num_ask = 1
        s.save()

    return JsonResponse(res)

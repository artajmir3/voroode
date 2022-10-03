from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

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
    res = {'res':False}
    for user in response.json()['data']:
        if username == user['username']:
            res['res'] = True

    return JsonResponse(res)

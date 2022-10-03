from django.conf.urls import url
from herokuapp.views import hey_view

urlpatterns = [
    url('hey/', hey_view, name='hey'),
]

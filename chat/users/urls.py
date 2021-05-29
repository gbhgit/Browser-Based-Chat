# users/urls.py

from django.conf.urls import include, url
from users.views import home, register, index

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^home/", home, name="home"),
    url(r"^register/", register, name="register"),
    url(r"^", index, name="index"),
]
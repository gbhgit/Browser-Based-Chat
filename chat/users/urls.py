from django.conf.urls import include, url
from users.views import register, index, register_room


urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    #url(r"^home/", home, name="home"),
    url(r"^register/", register, name="register"),
    url(r"^room/", register_room, name="register_room"),
    url(r"^", index, name="index"),
]
from django.urls import path
from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("users.urls")),
    url(r"^admin/", admin.site.urls),
    # path('admin/', admin.site.urls),
]
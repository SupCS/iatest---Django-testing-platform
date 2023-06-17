from django.urls import include, path

from .views import RegisterView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", RegisterView.as_view(), name="register"),
]

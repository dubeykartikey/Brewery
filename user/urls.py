from . import views
from django.urls import path


urlpatterns = [
    path("", views.auth, name="auth"),
    path("login/", views.signin, name="login"),
    path("logout/", views.signout, name="logout"),
    path("home/", views.home, name="home"),
    path("filter/", views.filter, name="filter"),
    path("<uuid:id>/review/", views.review, name="review"),
]
 
from . import views
from django.urls import path


urlpatterns = [
    path('', views.signup, name='home'),
    path('login/', views.signin, name='login')
]
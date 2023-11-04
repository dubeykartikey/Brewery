from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.models import User

from user.models import Review
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import requests
from django.template.defaulttags import register


@register.filter
def get_range(value):
    return range(value)


def request_to_api(method, url):
    response = None
    if method == "get":
        response = requests.get(url)
    elif method == "post":
        response = requests.post(url)
    return response


@login_required(login_url="/")
def home(request):
    filters = ["by_city", "by_name", "by_type"]
    return render(request, "./home.html", context={"filters": filters, "breweries": []})


def auth(request):
    signin_form = LoginForm()
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect("home")
    else:
        signup_form = SignupForm()
    return render(
        request, "./auth.html", {"signup_form": signup_form, "signin_form": signin_form}
    )


def signin(request):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                message = f"Hello {user.username}! You have been logged in"
                return redirect("home")
            else:
                message = "Login failed!"
    return redirect("signup")


def filter(request):
    if request.method == "POST":
        values = request.POST
        filter, search = values.get("filter"), values.get("search")
        url = f"https://api.openbrewerydb.org/v1/breweries?{filter}={search}"

        response = request_to_api("get", url)
        print(response.json())
        return render(
            request,
            "./home.html",
            context={
                "breweries": response.json(),
                "filters": ["by_city", "by_name", "by_type"],
            },
        )

    return redirect("home")


def review(request, id):
    if request.method == "POST":
        values = request.POST
        rating, description = values.get("rating"), values.get("description")
        try:
            user = User.objects.get(username=request.user)
            review = Review.objects.create(
                brewery_id=id, user=user, rating=rating, description=description
            )
            review.save()
        except:
            pass

    url = f"https://api.openbrewerydb.org/v1/breweries/{id}"
    response = request_to_api("get", url)
    all_reviews = Review.objects.filter(brewery_id=id)
    return render(
        request,
        "review.html",
        context={
            "brewery": response.json(),
            "reviews": all_reviews,
        },
    )

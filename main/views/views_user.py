from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from main.forms import *


def login_page(request):
    page = "login"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "Потребителят не съществува!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")

        else:
            messages.error(request, "Грешно потребителско име или неправилна парола!")

    context = {"page": page}

    return render(request, "main/form_templates/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("index")


def register_page(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect("index")

        else:
            messages.error(request, "Настъпи грешка при регистрацията!")

    context = {"form": form}

    return render(request, "main/form_templates/login_register.html", context)

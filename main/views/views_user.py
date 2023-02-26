from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q

from main.forms import *


# index view
def index(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    tournamets = Tournament.objects.filter(
        Q(name__icontains=q)
        | Q(hall__name__icontains=q)
        | Q(hall__location__icontains=q)
    )

    teams = Team.objects.filter(Q(name__icontains=q))

    matches = Match.objects.filter(
        Q(team1__name__icontains=q) | Q(team2__name__icontains=q)
    )

    players = Player.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )

    referees = Referee.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )

    context = {
        "tournamets": tournamets,
        "teams": teams,
        "matches": matches,
        "players": players,
        "referees": referees,
    }

    return render(request, "main/index.html", context)


# login view
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


# logout view
def logout_user(request):
    logout(request)
    return redirect("index")


# register view
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

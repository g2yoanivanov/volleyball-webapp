from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Model
from django.http import HttpResponse
from django.shortcuts import render, redirect

import random

from main.models import *
from main.forms import *


@staff_member_required
def myadmin(request):
    return render(request, "main/admin_templates/myadmin.html")


def add_staff(request, pk):
    user = User.objects.get(id=pk)
    user.is_staff = True
    user.save()
    return redirect("admin_users")


def remove_staff(request, pk):
    user = User.objects.get(id=pk)
    user.is_staff = False
    user.save()
    return redirect("admin_users")


@staff_member_required
def admin_users(request):
    users = User.objects.all()

    context = {"users": users}

    return render(request, "main/admin_templates/admin_users.html", context)


@staff_member_required
def admin_tournaments(request):
    tournaments = Tournament.objects.all()

    context = {"tournaments": tournaments}

    return render(request, "main/admin_templates/admin_tournaments.html", context)


@staff_member_required
def admin_matches(request):
    matches = Match.objects.all()

    context = {"matches": matches}

    return render(request, "main/admin_templates/admin_matches.html", context)


@staff_member_required
def admin_players(request):
    players = Player.objects.all()

    context = {"players": players}

    return render(request, "main/admin_templates/admin_players.html", context)


@staff_member_required
def admin_teams(request):
    teams = Team.objects.all()

    context = {"teams": teams}

    return render(request, "main/admin_templates/admin_teams.html", context)


@staff_member_required
def admin_halls(request):
    halls = Hall.objects.all()

    context = {"halls": halls}

    return render(request, "main/admin_templates/admin_halls.html", context)


@staff_member_required
def admin_referees(request):
    referees = Referee.objects.all()

    context = {"referees": referees}

    return render(request, "main/admin_templates/admin_referees.html", context)

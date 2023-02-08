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

from .models import *
from .forms import *


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

    return render(request, "main/login_register.html", context)


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

    return render(request, "main/login_register.html", context)

# admin views
@staff_member_required
def myadmin(request):
    return render(request, 'main/admin_templates/myadmin.html')

# index (homepage)
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


# tournament views
def tournament_info(request, pk):
    tournament = Tournament.objects.get(id=pk)
    referees = Referee.objects.filter(tournaments__in=[tournament])
    matches = Match.objects.filter(tournament=tournament)

    now = timezone.now()

    context = {
        "tournament": tournament,
        "matches": matches,
        "referees": referees,
        "now": now,
    }

    return render(request, "main/info_templates/tournament_info.html", context)


def tournaments(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    sort_by = request.GET.get("sort_by")
    if sort_by == "newest":
        get_tournaments = Tournament.objects.filter(
            Q(name__icontains=q)
            | Q(hall__name__icontains=q)
            | Q(hall__location__icontains=q)
        ).order_by("-opening_date")
    elif sort_by == "oldest":
        get_tournaments = Tournament.objects.filter(
            Q(name__icontains=q)
            | Q(hall__name__icontains=q)
            | Q(hall__location__icontains=q)
        ).order_by("opening_date")
    elif sort_by == "hall":
        get_tournaments = Tournament.objects.filter(
            Q(name__icontains=q)
            | Q(hall__name__icontains=q)
            | Q(hall__location__icontains=q)
        ).order_by("hall", "-opening_date")
    else:
        get_tournaments = Tournament.objects.filter(
            Q(name__icontains=q)
            | Q(hall__name__icontains=q)
            | Q(hall__location__icontains=q)
        )

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_tournaments, items)
    page = request.GET.get("page")
    tournaments = paginator.get_page(page)

    now = timezone.now()

    context = {"tournaments": tournaments, "now": now}

    return render(request, "main/info_templates/tournaments.html", context)


@staff_member_required
def create_tournament(request):
    title = "create"
    web_title = "Създаване на турнир"
    form = TournamentForm()

    if request.method == "POST":
        form = TournamentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tournaments")
        else:
            messages.error(request, "Възникна грешка при създаването на турнир")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def edit_tournament(request, pk):
    title = "edit"
    web_title = "Редактиране на турнир"

    tournament = Match.objects.get(id=pk)
    form = TournamentForm(instance=tournament)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        form = TournamentForm(request.POST, request.FILES, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect("tournaments")

        else:
            messages.error(request, "Възникна грешка при редактирането на турнира!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def delete_tournament(request, pk):
    tournament = Tournament.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        tournament.delete()
        return redirect("tournaments")

    context = {"obj": tournament}
    return render(request, "main/form_templates/delete.html", context)


# matches views
def match_info(request, pk):
    match = Match.objects.get(id=pk)
    last_matches = Match.objects.filter(
        (Q(team1=match.team1) & Q(team2=match.team2))
        | (Q(team1=match.team2) & Q(team2=match.team1))
    ).order_by("-date")[0:10]

    now = timezone.now()

    context = {"match": match, "last_matches": last_matches, "now": now}

    return render(request, "main/info_templates/match_info.html", context)


def results(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    sort_by = request.GET.get("sort_by")
    if sort_by == "newest":
        get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        ).order_by("-date")
    elif sort_by == "oldest":
        get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        ).order_by("date")
    else:
        get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        )

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_matches, items)
    page = request.GET.get("page")
    matches = paginator.get_page(page)

    now = timezone.now()

    context = {"matches": matches, "now": now}

    return render(request, "main/info_templates/results.html", context)


def fixtures(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    sort_by = request.GET.get("sort_by")
    if sort_by == "newest":
        get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        ).order_by("-date")
    elif sort_by == "oldest":
        get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        ).order_by("date")
    else:
        get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        )

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_matches, items)
    page = request.GET.get("page")
    matches = paginator.get_page(page)

    now = timezone.now()

    context = {"matches": matches, "now": now}

    return render(request, "main/info_templates/fixtures.html", context)


@staff_member_required
def create_fixture(request):
    title = "create"
    web_title = "Създаване на мач"
    form = MatchForm()

    prices = [10, 20, 25, 30, 35]

    if request.method == "POST":
        form = MatchForm(request.POST, request.FILES)
        if form.is_valid():
            fixture = form.save()
            hall = fixture.tournament.hall
            price = random.choice(prices)
            quantity = fixture.tournament.hall.max_seats
            ticket = Ticket.objects.create(
            match=fixture, hall=hall, price=price, quantity=quantity
        )
            return redirect("fixtures")
        else:
            messages.error(request, "Възникна грешка при създаването на мач")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def edit_fixture(request, pk):
    title = "edit"
    web_title = "Редактиране на мач"

    fixture = Match.objects.get(id=pk)
    form = MatchForm(instance=fixture)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        form = MatchForm(request.POST, request.FILES, instance=fixture)
        if form.is_valid():
            form.save()
            return redirect("fixtures")

        else:
            messages.error(request, "Възникна грешка при редактирането на мача!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def delete_fixture(request, pk):
    fixture = Match.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        fixture.delete()
        return redirect("fixtures")

    context = {"obj": fixture}
    return render(request, "main/form_templates/delete.html", context)


# team views
def team_info(request, pk):
    team = Team.objects.get(id=pk)
    players = Player.objects.filter(team=team)
    won_tournaments = Tournament.objects.filter(winner=team)

    context = {"team": team, "players": players, "won_tournaments": won_tournaments}

    return render(request, "main/info_templates/team_info.html", context)


def teams(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    sort_by = request.GET.get("sort_by")
    if sort_by == "name":
        get_teams = Team.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("name")
    elif sort_by == "newest":
        get_teams = Team.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("-founded_in")
    elif sort_by == "oldest":
        get_teams = Team.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("founded_in")
    elif sort_by == "location":
        get_teams = Team.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("location", "-founded_in")
    else:
        get_teams = Team.objects.filter(Q(name__icontains=q) | Q(location__icontains=q))

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_teams, items)
    page = request.GET.get("page")
    teams = paginator.get_page(page)

    context = {"teams": teams}

    return render(request, "main/info_templates/teams.html", context)


@staff_member_required
def create_team(request):
    title = "create"
    web_title = "Създаване на отбор"
    form = TeamForm()

    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("teams")
        else:
            messages.error(request, "Възникна грешка при създаването на отбор")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def edit_team(request, pk):
    title = "edit"
    web_title = "Редактиране на отбор"

    team = Team.objects.get(id=pk)
    form = TeamForm(instance=team)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect("teams")

        else:
            messages.error(request, "Възникна грешка при редактирането на отбора!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def delete_team(request, pk):
    team = Team.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if team.picture:
            team.picture.storage.delete(team.picture.path)
        team.delete()
        return redirect("teams")

    context = {"obj": team}
    return render(request, "main/form_templates/delete.html", context)


# players views
def player_info(request, pk):
    player = Player.objects.get(id=pk)

    context = {"player": player}

    return render(request, "main/info_templates/player_info.html", context)


def players(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    sort_by = request.GET.get("sort_by")
    if sort_by == "name":
        get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        ).order_by("first_name", "last_name")
    elif sort_by == "team":
        get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        ).order_by("team", "first_name", "last_name")
    elif sort_by == "youngest":
        get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        ).order_by("age")
    elif sort_by == "oldest":
        get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        ).order_by("-age")
    elif sort_by == "position":
        get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        ).order_by("position")
    else:
        get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        )

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_players, items)
    page = request.GET.get("page")
    players = paginator.get_page(page)

    context = {"players": players, "teams": teams}

    return render(request, "main/info_templates/players.html", context)


@staff_member_required
def create_player(request):
    title = "create"
    web_title = "Създаване на играч"
    form = PlayerForm()

    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("players")
        else:
            messages.error(request, "Възникна грешка при създаването на играч")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def edit_player(request, pk):
    title = "edit"
    web_title = "Редактиране на играч"

    player = Player.objects.get(id=pk)
    form = PlayerForm(instance=player)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect("players")

        else:
            messages.error(request, "Възникна грешка при редактирането на играча!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def delete_player(request, pk):
    player = Player.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if player.photo:
            player.photo.storage.delete(player.photo.path)
        player.delete()
        return redirect("players")

    context = {"obj": player}
    return render(request, "main/form_templates/delete.html", context)


# referees views
def referees(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    now = timezone.now()

    sort_by = request.GET.get("sort_by")
    if sort_by == "name":
        get_referees = Referee.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        ).order_by("first_name", "last_name")
    elif sort_by == "nationality":
        get_referees = Referee.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        ).order_by("nationality")
    elif sort_by == "experience":
        get_referees = Referee.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        ).order_by("-experience")
    else:
        get_referees = Referee.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_referees, items)
    page = request.GET.get("page")
    referees = paginator.get_page(page)

    context = {"referees": referees}

    return render(request, "main/info_templates/referees.html", context)


@staff_member_required
def create_referee(request):
    title = "create"
    web_title = "Създаване на съдия"
    form = RefereeForm()

    if request.method == "POST":
        form = RefereeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("referees")
        else:
            messages.error(request, "Възникна грешка при създаването на зала")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def edit_referee(request, pk):
    title = "edit"
    web_title = "Редактиране на съдия"

    referee = Referee.objects.get(id=pk)
    form = RefereeForm(instance=referee)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        form = RefereeForm(request.POST, request.FILES, instance=referee)
        if form.is_valid():
            form.save()
            return redirect("referees")

        else:
            messages.error(request, "Възникна грешка при редактирането на залата!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def delete_referee(request, pk):
    referee = Referee.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if referee.photo:
            referee.photo.storage.delete(referee.photo.path)
        referee.delete()
        return redirect("referees")

    context = {"obj": referee}
    return render(request, "main/form_templates/delete.html", context)


# halls views
def halls(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    sort_by = request.GET.get("sort_by")
    if sort_by == "name":
        get_halls = Hall.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("name")
    elif sort_by == "seats":
        get_halls = Hall.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("max_seats")
    elif sort_by == "location":
        get_halls = Hall.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        ).order_by("location")
    else:
        get_halls = Hall.objects.filter(Q(name__icontains=q) | Q(location__icontains=q))

    show = request.GET.get("show")
    if show == "18":
        items = 18
    elif show == "30":
        items = 30
    elif show == "60":
        items = 60
    else:
        items = 18

    paginator = Paginator(get_halls, items)
    page = request.GET.get("page")
    halls = paginator.get_page(page)

    tournaments = Tournament.objects.all()

    context = {"halls": halls, "tournaments": tournaments}

    return render(request, "main/info_templates/halls.html", context)


@staff_member_required
def create_hall(request):
    title = "create"
    web_title = "Създаване на зала"
    form = HallForm()

    if request.method == "POST":
        form = HallForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("halls")
        else:
            messages.error(request, "Възникна грешка при създаването на зала")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def edit_hall(request, pk):
    title = "edit"
    web_title = "Редактиране на зала"

    hall = Hall.objects.get(id=pk)
    form = HallForm(instance=hall)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        form = HallForm(request.POST, request.FILES, instance=hall)
        if form.is_valid():
            form.save()
            return redirect("halls")

        else:
            messages.error(request, "Възникна грешка при редактирането на залата!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/creation_form.html", context)


@staff_member_required
def delete_hall(request, pk):
    hall = Hall.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if hall.picture:
            hall.picture.storage.delete(hall.picture.path)
        hall.delete()
        return redirect("halls")

    context = {"obj": hall}
    return render(request, "main/form_templates/delete.html", context)

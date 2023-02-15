
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from main.forms import *


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

    context = {"players": players}

    return render(request, "main/info_templates/players.html", context)


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

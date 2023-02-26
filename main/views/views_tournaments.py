from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from main.forms import *


# Read
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


# Read all
def tournaments(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    get_tournaments = Tournament.objects.filter(
            Q(name__icontains=q)
            | Q(hall__name__icontains=q)
            | Q(hall__location__icontains=q)
        )

    sort_by = request.GET.get("sort_by")

    if sort_by == "newest":
        get_tournaments = get_tournaments.order_by("-opening_date")

    elif sort_by == "oldest":
        get_tournaments.order_by("opening_date")

    elif sort_by == "hall":
        get_tournaments.order_by("hall", "-opening_date")

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


# Create
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


# Update
@staff_member_required
def edit_tournament(request, pk):
    title = "edit"
    web_title = "Редактиране на турнир"

    tournament = Tournament.objects.get(id=pk)
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


# Delete
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

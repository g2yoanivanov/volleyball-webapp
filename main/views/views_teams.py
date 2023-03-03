from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from main.forms import *


# Read
def team_info(request, pk):
    team = Team.objects.get(id=pk)
    players = Player.objects.filter(team=team)
    won_tournaments = Tournament.objects.filter(winner=team)

    context = {"team": team, "players": players, "won_tournaments": won_tournaments}

    return render(request, "main/info_templates/team_info.html", context)


# Read all
def teams(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    get_teams = Team.objects.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        )

    sort_by = request.GET.get("sort_by")

    if sort_by == "name":
        get_teams = get_teams.order_by("name")
        
    elif sort_by == "newest":
        get_teams = get_teams.order_by("-founded_in")

    elif sort_by == "oldest":
        get_teams = get_teams.order_by("founded_in")

    elif sort_by == "location":
        get_teams = get_teams.order_by("location", "-founded_in")

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


# Create
@staff_member_required
def create_team(request):
    title = "create"
    web_title = "Създаване на отбор"
    form = TeamForm()

    if request.method == "POST":
        try:
            picture = request.FILES.get("picture")

            Hall.objects.create(
                name=request.POST.get("name"),
                coach=request.POST.get("coach"),
                location=request.POST.get("location"),
                founded_in=request.POST.get("founded_in"),
                picture=picture,
                description=request.POST.get("description"),
            )

            return redirect("teams")

        except:
            messages.error(request, "Възникна грешка при създаването на отбор!")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/team_form.html", context)


# Update
@staff_member_required
def edit_team(request, pk):
    title = "edit"
    web_title = "Редактиране на отбор"
    now = timezone.now()

    team = Team.objects.get(id=pk)
    form = TeamForm(instance=team)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:
            picture = request.FILES.get("picture")

            if picture: 
                team.name=request.POST.get("name")
                team.location=request.POST.get("location")
                team.coach=request.POST.get("coach")
                team.founded_in=request.POST.get("founded_in")
                team.description=request.POST.get("description")
                team.picture=picture
                team.save()
            
            else:
                team.name=request.POST.get("name")
                team.location=request.POST.get("location")
                team.coach=request.POST.get("coach")
                team.founded_in=request.POST.get("founded_in")
                team.description=request.POST.get("description")
                team.save()
            
            return redirect("teams")

        except:
            messages.error(request, "Възникна грешка при създаването на отбор!")

    context = {"title": title, "form": form, "web_title": web_title, "team": team, "now": now}
    return render(request, "main/form_templates/team_form.html", context)


# Delete
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

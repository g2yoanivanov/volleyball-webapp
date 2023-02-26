from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from main.forms import *


# Read
def player_info(request, pk):
    player = Player.objects.get(id=pk)

    context = {"player": player}

    return render(request, "main/info_templates/player_info.html", context)


# Read all
def players(request):
    # query from the search bar
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    get_players = Player.objects.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(team__name__icontains=q)
        )

    sort_by = request.GET.get("sort_by")
    
    if sort_by == "name":
        get_players = get_players.order_by("first_name", "last_name")

    elif sort_by == "team":
        get_players = get_players.order_by("team", "first_name", "last_name")

    elif sort_by == "youngest":
        get_players = get_players.order_by("-birth_date")

    elif sort_by == "oldest":
       get_players = get_players.order_by("birth_date")

    elif sort_by == "position":
        get_players = get_players.order_by("position")
        

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


# Create
@staff_member_required
def create_player(request):
    title = "create"
    web_title = "Създаване на играч"
    now = timezone.now()

    teams = Team.objects.all()
    form = PlayerForm()

    if request.method == "POST":
        try:
            team_name = request.POST.get("team")
            team = Team.objects.get(name=team_name)
            photo = request.FILES.get("photo")

            Player.objects.create(
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                birth_date=request.POST.get("birth_date"),
                height=request.POST.get("height"),
                nationality=request.POST.get("nationality"),
                position=request.POST.get("position"),
                team=team,
                photo=photo,
                description=request.POST.get("description"),
            )

            return redirect("players")

        except:
            messages.error(request, "Въведеният отбор не съществува!")

    context = {
        "form": form,
        "title": title,
        "web_title": web_title,
        "teams": teams,
        "now": now,
    }
    return render(request, "main/form_templates/player_form.html", context)


# Update
@staff_member_required
def edit_player(request, pk):
    title = "edit"
    web_title = "Редактиране на играч"
    now = timezone.now()

    teams = Team.objects.all()

    player = Player.objects.get(id=pk)
    form = PlayerForm(instance=player)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:
            team_name = request.POST.get("team")
            team = Team.objects.get(name=team_name)

            photo = request.FILES.get("photo")

            if photo:
                player.first_name=request.POST.get("first_name")
                player.last_name=request.POST.get("last_name")
                player.birth_date=request.POST.get("birth_date")
                player.height=request.POST.get("height")
                player.nationality=request.POST.get("nationality")
                player.position=request.POST.get("position")
                player.team=team
                player.photo = photo
                player.description=request.POST.get("description")
                player.save()

            else:
                player.first_name=request.POST.get("first_name")
                player.last_name=request.POST.get("last_name")
                player.birth_date=request.POST.get("birth_date")
                player.height=request.POST.get("height")
                player.nationality=request.POST.get("nationality")
                player.position=request.POST.get("position")
                player.team=team
                player.description=request.POST.get("description")
                player.save()
                
            return redirect("players")

        except:
            messages.error(request, "Въведеният отбор не съществува!")

    context = {
        "title": title,
        "form": form,
        "web_title": web_title,
        "teams": teams,
        "player": player,
        "now": now,
    }
    return render(request, "main/form_templates/player_form.html", context)


# Delete
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
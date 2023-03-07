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
    teams = Team.objects.filter(tournaments__in=[tournament])

    now = timezone.now()

    context = {
        "tournament": tournament,
        "teams": teams,
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
        get_tournaments = get_tournaments.order_by("opening_date")

    elif sort_by == "hall":
        get_tournaments = get_tournaments.order_by("hall", "-opening_date")

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

    teams = Team.objects.all()
    referees = Referee.objects.all()
    halls = Hall.objects.all()

    form = TournamentForm()

    if request.method == "POST":
        try:
            selected_teams_names = request.POST.getlist("selected_teams")
            selected_teams = Team.objects.filter(name__in=selected_teams_names)

            selected_referees_ids = request.POST.getlist("selected_referees")
            selected_referees = Referee.objects.filter(id__in=selected_referees_ids)

            hall_name = request.POST.get("hall")
            hall = Hall.objects.get(name=hall_name)

            tournament=Tournament.objects.create(
                name=request.POST.get("name"),
                hall=hall,
                opening_date=request.POST.get("opening_date"),
                closing_date=request.POST.get("closing_date"), 
                prize_pool=request.POST.get("prize_pool"),
                description=request.POST.get("description")  
            )
            tournament.teams.set(selected_teams)
            tournament.referees.set(selected_referees)

            return redirect("tournaments")
        
        except Exception as e:
            messages.error(request, '{}'.format(str(e)))
            

    context = {
            "form": form,
            "title": title, 
            "web_title": web_title, 
            "teams": teams, 
            "referees": referees,
            "halls": halls
        }
    
    return render(request, "main/form_templates/tournament_form.html", context)


# Update
@staff_member_required
def edit_tournament(request, pk):
    title = "edit"
    web_title = "Редактиране на турнир"
    now = timezone.now()

    tournament = Tournament.objects.get(id=pk)
    form = TournamentForm(instance=tournament)

    teams_in_tournament = Team.objects.filter(tournaments__in=[tournament])
    teams = Team.objects.all()
    referees = Referee.objects.all()
    halls = Hall.objects.all()

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:
            selected_teams_names = request.POST.getlist("selected_teams")
            selected_teams = Team.objects.filter(name__in=selected_teams_names)

            selected_referees_ids = request.POST.getlist("selected_referees")
            selected_referees = Referee.objects.filter(id__in=selected_referees_ids)

            hall_name = request.POST.get("hall")
            hall = Hall.objects.get(name=hall_name)

            winner_name = request.POST.get("winner")
            if winner_name is not None:
                winner = Team.objects.get(name=winner_name)
            else:
                winner = None
            
            if winner is not None:
                tournament.name=request.POST.get("name")
                tournament.hall=hall
                tournament.opening_date=request.POST.get("opening_date")
                tournament.closing_date=request.POST.get("closing_date")
                tournament.prize_pool=request.POST.get("prize_pool")
                tournament.description=request.POST.get("description")
                tournament.winner = winner
                tournament.save()
            
            else:
                tournament.name=request.POST.get("name")
                tournament.hall=hall
                tournament.opening_date=request.POST.get("opening_date")
                tournament.closing_date=request.POST.get("closing_date")
                tournament.prize_pool=request.POST.get("prize_pool")
                tournament.description=request.POST.get("description")
                tournament.save()

            tournament.teams.set(selected_teams)
            tournament.referees.set(selected_referees)
            return redirect("tournaments")
        
        except Exception as e:
            messages.error(request, '{}'.format(str(e)))


    context = {
            "title": title, 
            "form": form, 
            "web_title": web_title,
            "now": now,
            "tournament": tournament,
            "teams": teams,
            "halls": halls,
            "referees": referees,
            "teams_in_tournament": teams_in_tournament
        }
    return render(request, "main/form_templates/tournament_form.html", context)


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

from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse


import random

from main.forms import *

# Read
def match_info(request, pk):
    match = Match.objects.get(id=pk)
    last_matches = Match.objects.filter(
        (Q(team1=match.team1) & Q(team2=match.team2))
        | (Q(team1=match.team2) & Q(team2=match.team1))
    ).order_by("-date")[0:10]

    now = timezone.now()

    user = request.user

    context = {"match": match, "last_matches": last_matches, "now": now}

    return render(request, "main/info_templates/match_info.html", context)


# Read all (matches in the past)
def results(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        )

    sort_by = request.GET.get("sort_by")

    if sort_by == "newest":
        get_matches = get_matches.order_by("-date")

    elif sort_by == "oldest":
        get_matches = get_matches.order_by("date")

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


# Read all (matches in the future)
def fixtures(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    get_matches = Match.objects.filter(
            Q(team1__name__icontains=q)
            | Q(team2__name__icontains=q)
            | Q(tournament__name__icontains=q)
        )

    sort_by = request.GET.get("sort_by")

    if sort_by == "newest":
        get_matches = get_matches.order_by("-date")

    elif sort_by == "oldest":
        get_matches = get_matches.order_by("date")

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


# Create
@staff_member_required
def create_fixture(request):
    title = "create"
    web_title = "Създаване на мач"
    form = MatchForm()

    prices = [10, 20, 25, 30, 35]
    now = timezone.now()

    teams = Team.objects.all()
    referees = Referee.objects.all()
    tournaments = Tournament.objects.all()

    if request.method == "POST":
        try:
            team1_name = request.POST.get("team1")
            team1 = Team.objects.get(name=team1_name)

            team2_name = request.POST.get("team2")
            team2 = Team.objects.get(name=team2_name)

            tournament_name = request.POST.get("tournament")
            tournament = Tournament.objects.get(name=tournament_name)

            ref_name = request.POST.get("referee").split(" ")
            referee_first_name = ref_name[0]
            referee_last_name = ref_name[1]
            referee = Referee.objects.get(
                first_name=referee_first_name, last_name=referee_last_name
            )

            if team1 != team2:
                fixture = Match.objects.create(
                    team1=team1,
                    team2=team2,
                    tournament=tournament,
                    date=request.POST.get("date"),
                    referee=referee,
                )

                hall = fixture.tournament.hall
                price = random.choice(prices)
                quantity = fixture.tournament.hall.max_seats
                Ticket.objects.create(
                    match=fixture, hall=hall, price=price, quantity=quantity
                )
                return redirect("fixtures")
            else:
                messages.error(request, "Двата отбора в мача трябва да са различни!")

        except Exception as e:
            messages.error(request, '{}'.format(str(e)))

    context = {
        "form": form,
        "title": title,
        "web_title": web_title,
        "now": now,
        "teams": teams,
        "tournaments": tournaments,
        "referees": referees,
    }
    return render(request, "main/form_templates/match_form.html", context)


# Update
@staff_member_required
def edit_fixture(request, pk):
    title = "edit"
    web_title = "Редактиране на мач"
    now = timezone.now()

    fixture = Match.objects.get(id=pk)
    form = MatchForm(instance=fixture)

    teams = Team.objects.all()
    referees = Referee.objects.all()
    tournaments = Tournament.objects.all()

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:
            team1_name = request.POST.get("team1")
            team1 = Team.objects.get(name=team1_name)

            team2_name = request.POST.get("team2")
            team2 = Team.objects.get(name=team2_name)

            tournament_name = request.POST.get("tournament")
            tournament = Tournament.objects.get(name=tournament_name)

            ref_name = request.POST.get("referee").split(" ")
            referee_first_name = ref_name[0]
            referee_last_name = ref_name[1]
            referee = Referee.objects.get(
                first_name=referee_first_name, last_name=referee_last_name
            )

            date = request.POST.get("date")

            team1_points = request.POST.get("team1_points")
            team2_points = request.POST.get("team2_points")

            team1_won_with_25 = False
            team2_won_with_25 = False
            team1_won_more_25 = False
            team2_won_more_25 = False

            if team1_points and team2_points:
                team1_points = int(team1_points)
                team2_points = int(team2_points)

                if team1_points == 25 and 0 <= team2_points < 24:
                    team1_won_with_25 = True

                elif team2_points == 25 and 0 <= team1_points < 24:
                    team2_won_with_25 = True
                
                elif team1_points > 25 and team2_points > 25 and team1_points - team2_points == 2:
                    team1_won_more_25 = True

                elif team1_points > 25 and team2_points > 25 and team2_points - team1_points == 2:
                    team2_won_more_25 = True

            if team1_points and team2_points:
                if team1_won_with_25 or team2_won_with_25 or team1_won_more_25 or team2_won_more_25:
                    fixture.team1=team1
                    fixture.team2=team2
                    fixture.tournament=tournament
                    fixture.date=date
                    fixture.referee=referee
                    fixture.team1_points=team1_points
                    fixture.team2_points=team2_points
                    fixture.save()

                else:
                    messages.error(request, "Въведен е невалиден резултат!")

            else:
                fixture.team1=team1
                fixture.team2=team2
                fixture.tournament=tournament
                fixture.date=request.POST.get("date")
                fixture.referee=referee
                fixture.save()

            return redirect("fixtures")

        except Exception as e:
            messages.error(request, '{}'.format(str(e)))

    context = {
        "title": title,
        "form": form,
        "web_title": web_title,
        "now": now,
        "teams": teams,
        "tournaments": tournaments,
        "referees": referees,
        "match": fixture,
    }

    return render(request, "main/form_templates/match_form.html", context)

@staff_member_required()
def edit_ticket(request, pk):
    ticket = Ticket.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:
            ticket.price = request.POST.get("price")
            ticket.quantity = request.POST.get("quantity")
            ticket.save()

            return redirect('fixtures')

        except Exception as e:
            messages.error(request, '{}'.format(str(e)))

    context = {"ticket": ticket}

    return render(request, 'main/form_templates/ticket_price_form.html', context)

# Delete
@staff_member_required
def delete_fixture(request, pk):
    fixture = Match.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        fixture.delete()
        if fixture.ticket.qr_code:
            image_path = os.path.abspath(os.path.join(settings.BASE_DIR, "static", "images", fixture.ticket.qr_code.name))
            os.remove(image_path)

            fixture.ticket.qr_code.storage.delete(fixture.ticket.qr_code.name)
        fixture.ticket.delete()
        return redirect("fixtures")

    context = {"obj": fixture}
    return render(request, "main/form_templates/delete.html", context)

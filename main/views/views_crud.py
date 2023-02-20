from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

import random

from main.forms import *

# region TOURNAMENTS
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


# endregion

# region MATCHES
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
        team1_name = request.POST.get("team1")
        team1 = Team.objects.get(name=team1_name).exists()

        team2_name = request.POST.get("team2")
        team2 = Team.objects.get(name=team2_name).exists()

        tournament_name = request.POST.get("tournament")
        tournament = Tournament.objects.get(name=tournament_name).exists()

        ref_name = request.POST.get("referee")
        referee = Referee.objects.get(name=ref_name).exists()

        if team1 and team2 and tournament and referee:
            fixture = Match.objects.create(
                team1 = team1,
                team2 = team2,
                tournament = tournament,
                date = request.POST.get("birth_date"),
                referee = referee,
            )

            hall = fixture.tournament.hall
            price = random.choice(prices)
            quantity = fixture.tournament.hall.max_seats
            Ticket.objects.create(
                match=fixture,
                hall=hall,
                price=price,
                quantity=quantity
            )
            return redirect("fixtures")
        
        else:
            messages.error(request, "Възникна грешка при създаването на мач! Проверете: 'Отбор 1', 'Отбор 2', 'Турнир', 'Съдия'")


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


@staff_member_required
def edit_fixture(request, pk):
    title = "edit"
    web_title = "Редактиране на мач"

    fixture = Match.objects.get(id=pk)
    form = MatchForm(instance=fixture)

    teams = Team.objects.all()
    referees = Referee.objects.all()
    tournaments = Tournament.objects.all()

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        team1_name = request.POST.get("team1")
        team1 = Team.objects.get(name=team1_name).exists()

        team2_name = request.POST.get("team2")
        team2 = Team.objects.get(name=team2_name).exists()

        tournament_name = request.POST.get("tournament")
        tournament = Tournament.objects.get(name=tournament_name).exists()

        ref_name = request.POST.get("referee").split(' ')
        referee = Referee.objects.get(first_name=ref_name[0]).exists()

        if team1 and team2 and tournament and referee and team1 is not team2:
            fixture = Match.objects.update(
                team1 = team1,
                team2 = team2,
                tournament = tournament,
                date = request.POST.get("birth_date"),
                referee = referee,
            )

            return redirect("fixtures")
        
        else:
            messages.error(request, "Възникна грешка при създаването на мач! Проверете: 'Отбор 1', 'Отбор 2', 'Турнир', 'Съдия'")

    context = {
        "title": title,
        "form": form,
        "web_title": web_title,
        "teams": teams,
        "tournaments": tournaments,
        "referees": referees,
    }
    return render(request, "main/form_templates/match_form.html", context)


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


# endregion

# region TEAMS
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


# endregion

# region PLAYERS
@staff_member_required
def create_player(request):
    title = "create"
    web_title = "Създаване на играч"
    now = timezone.now()

    teams = Team.objects.all()
    form = PlayerForm()

    if request.method == "POST":
        team_name = request.POST.get("team")
        team = Team.objects.get(name=team_name)
        photo = request.FILES.get("photo")

        try:
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
        team_name = request.POST.get("team")
        team = Team.objects.get(name=team_name).exists()

        photo = request.FILES.get("photo")

        if team:
            if photo:
                player = Player.objects.update(
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
            else:
                player = Player.objects.update(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    birth_date=request.POST.get("birth_date"),
                    height=request.POST.get("height"),
                    nationality=request.POST.get("nationality"),
                    position=request.POST.get("position"),
                    team=team,
                    description=request.POST.get("description"),
                )

            return redirect("players")

        else:
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


# endregion

# region REFEREES
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


# endregion

# region HALLS
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


# endregion

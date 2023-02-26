from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from main.forms import *


# Read all
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


# Create
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


# Update
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


# Delete
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

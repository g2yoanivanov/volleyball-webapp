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

    get_referees = Referee.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )

    sort_by = request.GET.get("sort_by")
    if sort_by == "name":
       get_referees = get_referees.order_by("first_name", "last_name")
       
    elif sort_by == "nationality":
        get_referees = get_referees.order_by("nationality")

    elif sort_by == "experience":
        get_referees = get_referees.order_by("-experience")

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
@staff_member_required(login_url='access')
def create_referee(request):
    title = "create"
    web_title = "Създаване на съдия"
    now = timezone.now()

    form = RefereeForm()

    if request.method == "POST":
        try:
            photo = request.FILES.get("photo")

            if photo:
                Referee.objects.create(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    birth_date=request.POST.get("birth_date"),
                    experience=request.POST.get("experience"),
                    nationality=request.POST.get("nationality"),
                    photo=photo,
                    description=request.POST.get("description"),
                )
            else:
                Referee.objects.create(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    birth_date=request.POST.get("birth_date"),
                    experience=request.POST.get("experience"),
                    nationality=request.POST.get("nationality"),
                    description=request.POST.get("description"),
                )

            return redirect("referees")

        except:
            messages.error(request, "Възникна грешка при създаването на съдия!")

    context = {"form": form, "title": title, "web_title": web_title, "now": now}
    return render(request, "main/form_templates/referee_form.html", context)


# Update
@staff_member_required(login_url='access')
def edit_referee(request, pk):
    title = "edit"
    web_title = "Редактиране на съдия"
    now = timezone.now()

    referee = Referee.objects.get(id=pk)
    form = RefereeForm(instance=referee)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:

            photo = request.FILES.get("photo")

            if photo:
                referee.first_name=request.POST.get("first_name")
                referee.last_name=request.POST.get("last_name")
                referee.birth_date=request.POST.get("birth_date")
                referee.experience=request.POST.get("experience")
                referee.nationality=request.POST.get("nationality")
                referee.photo=photo
                referee.description=request.POST.get("description")
                referee.save()

            else:
                referee.first_name=request.POST.get("first_name")
                referee.last_name=request.POST.get("last_name")
                referee.birth_date=request.POST.get("birth_date")
                referee.experience=request.POST.get("experience")
                referee.nationality=request.POST.get("nationality")
                referee.description=request.POST.get("description")
                referee.save()

            return redirect("referees")

        except:
            messages.error(request, "Възникна грешка при създаването на съдия!")

    context = {"title": title, "form": form, "web_title": web_title, "now": now, "referee": referee}
    return render(request, "main/form_templates/referee_form.html", context)


# Delete
@staff_member_required(login_url='access')
def delete_referee(request, pk):
    referee = Referee.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if referee.photo:
            image_path = os.path.abspath(os.path.join(settings.BASE_DIR, "static", "images", referee.photo.name))
            os.remove(image_path)

            referee.photo.storage.delete(referee.photo.name)
        referee.delete()
        return redirect("referees")

    context = {"obj": referee}
    return render(request, "main/form_templates/delete.html", context)

from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from main.forms import *


# Read all
def halls(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    get_halls = Hall.objects.filter(
            Q(name__icontains=q) 
            | Q(location__icontains=q)
        )

    sort_by = request.GET.get("sort_by")

    if sort_by == "name":
        get_halls = get_halls.order_by("name")

    elif sort_by == "seats":
        get_halls = get_halls.order_by("max_seats")
        
    elif sort_by == "location":
        get_halls = get_halls.order_by("location")

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


# Create
@staff_member_required
def create_hall(request):
    title = "create"
    web_title = "Създаване на зала"
    form = HallForm()

    if request.method == "POST":
        try:
            picture = request.FILES.get("picture")

            Hall.objects.create(
                name=request.POST.get("name"),
                location=request.POST.get("location"),
                max_seats=request.POST.get("max_seats"),
                picture=picture,
            )

            return redirect("halls")

        except:
            messages.error(request, "Възникна грешка при създаването на зала!")

    context = {"form": form, "title": title, "web_title": web_title}
    return render(request, "main/form_templates/hall_form.html", context)


# Update
@staff_member_required
def edit_hall(request, pk):
    title = "edit"
    web_title = "Редактиране на зала"

    hall = Hall.objects.get(id=pk)
    form = HallForm(instance=hall)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        try:
            picture = request.FILES.get("picture")

            if picture: 
                hall.name=request.POST.get("name")
                hall.location=request.POST.get("location")
                hall.max_seats=request.POST.get("max_seats")
                hall.picture=picture
                hall.save()
            
            else:
                hall.name=request.POST.get("name")
                hall.location=request.POST.get("location")
                hall.max_seats=request.POST.get("max_seats")
                hall.save()
            
            return redirect("halls")

        except:
            messages.error(request, "Възникна грешка при създаването на зала!")

    context = {"title": title, "form": form, "web_title": web_title}
    return render(request, "main/form_templates/hall_form.html", context)


# Delete
@staff_member_required
def delete_hall(request, pk):
    hall = Hall.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if hall.picture:
            image_path = os.path.abspath(os.path.join(settings.BASE_DIR, "static", "images", hall.picture.name))
            os.remove(image_path)

            hall.picture.storage.delete(hall.picture.name)
        hall.delete()
        return redirect("halls")

    context = {"obj": hall}
    return render(request, "main/form_templates/delete.html", context)
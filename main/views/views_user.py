from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from main.forms import *


# index view
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


# login view
def login_page(request):
    page = "login"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, "Потребителят не съществува!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")

        else:
            messages.error(request, "Грешно потребителско име или неправилна парола!")

    context = {"page": page}

    return render(request, "main/form_templates/login_register.html", context)


# logout view
def logout_user(request):
    logout(request)
    return redirect("index")


# register view
def register_page(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        get_username = request.POST.get("username")
        try:
            check_user = User.objects.get_or_none(username=get_username)
        except:
            check_user = None

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect("index")

        else:
            if User.objects.filter(username=check_user.username).exists():
                messages.error(request, "Това потребителско име вече съществува!")

            else:
                messages.error(request, "Настъпи грешка при регистрацията!")

    context = {"form": form}

    return render(request, "main/form_templates/login_register.html", context)

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)

    context = {"user": user}

    return render(request, "main/user_profile.html", context)

def update_user(request, pk):
    user = User.objects.get(id=pk)

def delete_user(request, pk):
    user = User.objects.get(id=pk)

    if not request.user.is_staff:
        return HttpResponse("Нямате достъп до тази страница!")

    if request.method == "POST":
        if user.profile_picture:
            image_path = os.path.abspath(os.path.join(settings.BASE_DIR, "static", "images", user.profile_picture.name))
            os.remove(image_path)

            user.profile_picture.storage.delete(user.profile_picture.name)
        user.delete()
        return redirect("admin_users")

    context = {"obj": user}
    return render(request, "main/form_templates/delete.html", context)

@login_required(login_url='login')
def buy_ticket(request, pk):
    fixture = Match.objects.get(id=pk)

    context = {"match": fixture}

    return render(request, "main/buy_ticket.html", context)


def completed(request, pk):
    match = Match.objects.get(id=pk)
    ticket = match.ticket_set.first()
    user = request.user

    tickets_bought = request.POST.get("quantity")

    if tickets_bought is not None:
        quantity = int(tickets_bought)
        ticket.quantity = ticket.quantity - quantity
        ticket.save()

        email_title = "Поръчката е завършена!"
        email_body = f"""Вие успешно закупихте {quantity} билет(а) за мача '{ticket.match.team1.name} - {ticket.match.team2.name}'! Благодарим Ви, че избрахте нас!
        
        Дата: {ticket.match.date}
        Локация: {ticket.match.tournament.hall}"""

        send_email(email_title, email_body, user.email, ticket.qr_code.path, ticket)

        return redirect('fixtures')
    else:
        return redirect('index')

def send_email(subject, body, to_email, attachment_path, ticket):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'yoan040707@gmail.com'
    smtp_password = 'doovonblclvzkrmf'

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = smtp_username
    message['To'] = to_email

    body_text = MIMEText(body, _subtype='html')
    message.attach(body_text)

    # Add the attachment
    with open(attachment_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='image/png')
        attachment.add_header('Content-Disposition', 'attachment', filename=f'{ticket.id}.png')
        message.attach(attachment)

    smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    smtp_conn.starttls()
    smtp_conn.login(smtp_username, smtp_password)
    smtp_conn.sendmail(smtp_username, to_email, message.as_string())
    smtp_conn.quit()


    

    
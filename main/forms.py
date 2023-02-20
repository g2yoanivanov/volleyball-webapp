from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import password_validation
from .models import *


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Парола"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control bg-bg"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Потвърдете паролата"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control bg-bg"}
        ),
        strip=False,
        help_text=("Въведете същата парола!"),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Потребителско име",
            "email": "Поща",
            "first_name": "Име",
            "last_name": "Фамилия",
            "birth_date": "Дата на раждане",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "email": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "first_name": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "last_name": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control bg-bg"}),
        }


class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = "__all__"
        labels = {
            "name": "Име",
            "location": "Локация",
            "max_seats": "Брой седалки",
            "picture": "Снимка",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "location": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "max_seats": forms.NumberInput(attrs={"class": "form-control bg-bg"}),
            "picture": forms.FileInput(attrs={"class": "form-control bg-bg"}),
        }


class RefereeForm(ModelForm):
    class Meta:
        model = Referee
        fields = "__all__"
        labels = {
            "first_name": "Име",
            "last_name": "Фамилия",
            "birth_date": "Дата на раждане",
            "nationality": "Националност",
            "experience": "Години стаж",
            "photo": "Снимка",
            "description": "Описание",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
            "last_name": forms.TextInput(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control bg-bg"}),
            "nationality": forms.TextInput(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
            "experience": forms.NumberInput(attrs={"class": "form-control bg-bg"}),
            "photo": forms.FileInput(attrs={"class": "form-control bg-bg"}),
            "description": forms.Textarea(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
        }


class PlayerForm(ModelForm):
    POSITIONS = (
        ("L", "Либеро"),
        ("S", "Разпределител"),
        ("OH", "Посрещач"),
        ("OP", "Диагонал"),
        ("MB", "Център"),
    )
    position = forms.ChoiceField(
        choices=POSITIONS, widget=forms.Select(attrs={"class": "form-control bg-bg"}),
        label = "Позиция"
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}), 
        label = "Отбор"
    )

    class Meta:
        model = Player
        fields = "__all__"
        labels = {
            "first_name": "Име",
            "last_name": "Фамилия",
            "birth_date": "Дата на раждане",
            "nationality": "Националност",
            "height": "Височина",   
            "photo": "Снимка",
            "description": "Описание",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
            "last_name": forms.TextInput(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control bg-bg"}),
            "nationality": forms.TextInput(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
            "height": forms.NumberInput(attrs={"class": "form-control bg-bg", "min": "1", "max": "3", "autocomplete": "off"}),
            "photo": forms.FileInput(attrs={"class": "form-control bg-bg"}),
            "description": forms.Textarea(attrs={"class": "form-control bg-bg", "autocomplete": "off"}),
        }


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
        labels = {
            "name": "Име",
            "coach": "Треньор",
            "founded_in": "Основан през",
            "location": "Локация",
            "picture": "Снимка",
            "description": "Описание",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "coach": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "founded_in": forms.DateInput(attrs={"class": "form-control bg-bg"}),
            "location": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "picture": forms.ClearableFileInput(attrs={"class": "form-control bg-bg"}),
            "description": forms.Textarea(attrs={"class": "form-control bg-bg"}),
        }


class MatchForm(ModelForm):
    team1 = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}),
        label = "Отбор 1"
    )

    team2 = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}),
        label = "Отбор 2"
    )

    tournament = forms.ModelChoiceField(
        queryset=Tournament.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}),
        label = "Турнир"
    )

    referee = forms.ModelChoiceField(
        queryset=Referee.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}),
        label = "Съдия"
    )

    class Meta:
        model = Match
        fields = "__all__"
        labels = {
            "date": "Дата",
            "team1_points": "Точки на Отбор 1",
            "team2_points": "Точки на Отбор 2",
        }
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control bg-bg"}),
            "team1_points": forms.NumberInput(attrs={"class": "form-control bg-bg"}),
            "team2_points": forms.NumberInput(attrs={"class": "form-control bg-bg"}),
        }


class TournamentForm(forms.ModelForm):
    hall = forms.ModelChoiceField(
        queryset=Hall.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}),
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "bg-bg"}),
    )

    referees = forms.ModelMultipleChoiceField(
        queryset=Referee.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "bg-bg"}),
    )

    winner = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={"class": "form-control bg-bg"}),
        required=False
    )

    class Meta:
        model = Tournament
        fields = "__all__"
        labels = {
            "name": "Име",
            "hall": "Зала",
            "prize_pool": "Награден фонд",
            "opening_date": "Дата на откриване",
            "closing_date": "Дата на закриване",
            "teams": "Отбори",
            "referees": "Съдии",
            "winner": "Победител",
            "description": "Описание"
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control bg-bg"}),
            "prize_pool": forms.NumberInput(attrs={"class": "form-control bg-bg"}),
            "opening_date": forms.DateTimeInput(attrs={"class": "form-control bg-bg"}),
            "closing_date": forms.DateTimeInput(attrs={"class": "form-control bg-bg"}),
            "description": forms.Textarea(attrs={"class": "form-control bg-bg"}),
        }

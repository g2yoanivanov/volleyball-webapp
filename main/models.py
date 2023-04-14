from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.conf import settings

import uuid
import qrcode
import os

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics", null=True, blank=True, default="/default_images/user_pic.jpeg")

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Hall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    location = models.CharField(max_length=128, null=False, blank=False)
    max_seats = models.PositiveIntegerField(validators=[MaxValueValidator(50000), MinValueValidator(500)], null=False, blank=False)

    picture = models.ImageField(upload_to="halls_pics", null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.location}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    coach = models.CharField(max_length=64, null=True, blank=True)
    founded_in = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=64, null=False, blank=False)

    picture = models.ImageField(upload_to="teams_pics", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITIONS = (
        ('L', 'Либеро'),
        ('S', 'Разпределител'),
        ('OH', 'Посрещач'),
        ('OP',  'Диагонал'),
        ('MB', 'Център'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=64, null=False, blank=False)
    height = models.DecimalField(decimal_places=2, max_digits=3, validators=[MinValueValidator(1), MaxValueValidator(3)], null=False, blank = False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=3, choices=POSITIONS, null=True, blank=True)

    photo = models.ImageField(upload_to="players_pics", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering=['team', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Referee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=64, null=False, blank=False)
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(0)], default=0, null=True, blank=True)

    photo = models.ImageField(upload_to="refs_pics", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)
    prize_pool = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(100)], null=True, blank = True)
    opening_date = models.DateTimeField(null=True, blank=True)
    closing_date = models.DateTimeField(null=True, blank=True)
    teams = models.ManyToManyField(Team, related_name='tournaments')
    referees = models.ManyToManyField(Referee, related_name='tournaments')
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-opening_date']

    def __str__(self):
        return f"{self.name} - {self.hall}"


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team2')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateTimeField(null=True, blank=True)
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True, blank=True)
    team1_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200), MinValueValidator(0)], null=True, blank=True)
    team2_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200), MinValueValidator(0)], null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-date', 'tournament']

    def __str__(self):
        return f"{self.team1} - {self.team2}, {self.date.strftime('%d.%m.%Y')}"


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False, blank=False)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(5)], null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    qr_code = models.ImageField(upload_to="qr_codes", null=False, blank=False)

    def save(self, *args, **kwargs):
        url = f"http://127.0.0.1:8000/match-info/{self.match.id}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        filename = f"{self.id}.png"
        filepath = os.path.join(settings.MEDIA_ROOT, "qr_codes", filename)
        img.save(filepath)

        self.qr_code.name = f"qr_codes/{filename}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket for {self.match.team1} - {self.match.team2}"
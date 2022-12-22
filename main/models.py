from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #first_name - Abstract User
    #last_name - Abstract User
    #username - Abstract User
    #email - Abstract User
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Hall(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, null=False, blank=False)
    location = models.CharField(max_length=128, null=False, blank=False)
    max_seats = models.PositiveIntegerField(validators=[MaxValueValidator(50000), MinValueValidator(500)], null=False, blank=False)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    coach = models.CharField(max_length=64, null=True, blank=True)
    founded_in = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=64, null=False, blank=False)

    def __str__(self):
        return self.name


class Player(models.Model):
    POSITIONS = (
        ('L', 'Libero'),
        ('S', 'Setter'),
        ('OH', 'Outside Hitter'),
        ('OP', 'Opposite Hitter'),
        ('MB', 'Middle Blocker'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(1)], null=False, blank=False)
    nationality = models.CharField(max_length=64, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=3, choices=POSITIONS, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Referee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(1)], null=False, blank=False)
    nationality = models.CharField(max_length=64, null=False, blank=False)
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120), MinValueValidator(0)], default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, null=False, blank=False)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)
    prize_pool = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(100)], null=True, blank = True)
    opening_date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField(Team, related_name='tournaments')
    referees = models.ManyToManyField(Referee, related_name='tournaments')

    def __str__(self):
        return f"{self.name} - {self.hall}"


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, related_name='team2')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=False, blank=False)
    date = models.DateField(null=True, blank=True)
    referee = models.ForeignKey(Referee, on_delete=models.SET_NULL, null=True, blank=True)
    team1_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200), MinValueValidator(0)], null=True, blank=True)
    team2_points = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200), MinValueValidator(0)], null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['date', 'tournament']

    def __str__(self):
        return f"{self.team1} - {self.team2}"


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False, blank=False)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False, blank=False)
    #seat_number = models.PositiveIntegerField(null=False, blank=False, validators=[MaxValueValidator(hall.max_seats), MinValueValidator(1)])
    price = models.DecimalField(decimal_places=2, max_digits=5, validators=[MinValueValidator(5)], null=False, blank=False)
    qr_code = models.ImageField(null=False, blank=False)

    def __str__(self):
        return f"Ticket for {self.match.team1} - {self.match.team2}"
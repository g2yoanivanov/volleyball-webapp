from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),

    path('myadmin/', views.myadmin, name='myadmin'),
    path('myadmin/users/', views.admin_users, name='admin_users'),
    path('myadmin/tournaments/', views.admin_tournaments, name='admin_tournaments'),
    path('myadmin/matches/', views.admin_matches, name='admin_matches'),
    path('myadmin/teams/', views.admin_teams, name='admin_teams'),
    path('myadmin/players/', views.admin_players, name='admin_players'),
    path('myadmin/halls/', views.admin_halls, name='admin_halls'),
    path('myadmin/referees/', views.admin_referees, name='admin_referees'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('tournaments/', views.tournaments, name='tournaments'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('referees/', views.referees, name='referees'),
    path('halls/', views.halls, name='halls'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('results/', views.results, name='results'),

    path('match-info/<str:pk>/', views.match_info, name='match-info'),
    path('tournaments/<str:pk>/', views.tournament_info, name='tournament_info'),
    path('teams/<str:pk>/', views.team_info, name='team_info'),
    path('players/<str:pk>/', views.player_info, name='player_info'),

    path('create-hall/', views.create_hall, name='create-hall'),
    path('edit-hall/<str:pk>/', views.edit_hall, name='edit-hall'),
    path('delete-hall/<str:pk>/', views.delete_hall, name='delete-hall'),

    path('create-referee/', views.create_referee, name='create-referee'),
    path('edit-referee/<str:pk>/', views.edit_referee, name='edit-referee'),
    path('delete-referee/<str:pk>/', views.delete_referee, name='delete-referee'),

    path('create-player/', views.create_player, name='create-player'),
    path('edit-player/<str:pk>/', views.edit_player, name='edit-player'),
    path('delete-player/<str:pk>/', views.delete_player, name='delete-player'),

    path('create-team/', views.create_team, name='create-team'),
    path('edit-team/<str:pk>/', views.edit_team, name='edit-team'),
    path('delete-team/<str:pk>/', views.delete_team, name='delete-team'),

    path('create-fixture/', views.create_fixture, name='create-fixture'),
    path('edit-fixture/<str:pk>/', views.edit_fixture, name='edit-fixture'),
    path('delete-fixture/<str:pk>/', views.delete_fixture, name='delete-fixture'),
    
    path('create-tournament/', views.create_tournament, name='create-tournament'),
    path('edit-tournament/<str:pk>/', views.edit_tournament, name='edit-tournament'),
    path('delete-tournament/<str:pk>/', views.delete_tournament, name='delete-tournament'),
]
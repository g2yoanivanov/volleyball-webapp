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

    path('myadmin/users/add-staff-role/<str:pk>/', views.add_staff, name='add_staff'),
    path('myadmin/users/remove-staff-role/<str:pk>/', views.remove_staff, name='remove_staff'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
    path("delete-user/<str:pk>", views.delete_user, name="delete-user"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('user-update/<str:pk>', views.update_user, name="user-update"),
    path('ticket/buy/<str:pk>/', views.buy_ticket, name="buy_ticket"),

    path('tournaments/', views.tournaments, name='tournaments'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),
    path('referees/', views.referees, name='referees'),
    path('halls/', views.halls, name='halls'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('results/', views.results, name='results'),

    path('matches/info/<str:pk>/', views.match_info, name='match-info'),
    path('tournaments/<str:pk>/', views.tournament_info, name='tournament_info'),
    path('teams/<str:pk>/', views.team_info, name='team_info'),
    path('players/<str:pk>/', views.player_info, name='player_info'),

    path('halls-create/', views.create_hall, name='create-hall'),
    path('halls/edit/<str:pk>/', views.edit_hall, name='edit-hall'),
    path('halls/delete/<str:pk>/', views.delete_hall, name='delete-hall'),

    path('referees-create/', views.create_referee, name='create-referee'),
    path('referees/edit/<str:pk>/', views.edit_referee, name='edit-referee'),
    path('referees/delete/<str:pk>/', views.delete_referee, name='delete-referee'),

    path('players-create/', views.create_player, name='create-player'),
    path('players/edit/<str:pk>/', views.edit_player, name='edit-player'),
    path('players/delete/<str:pk>/', views.delete_player, name='delete-player'),

    path('teams-create/', views.create_team, name='create-team'),
    path('teams/edit/<str:pk>/', views.edit_team, name='edit-team'),
    path('teams/delete/<str:pk>/', views.delete_team, name='delete-team'),

    path('fixtures-create/', views.create_fixture, name='create-fixture'),
    path('fixtures/edit/<str:pk>/', views.edit_fixture, name='edit-fixture'),
    path('fixtures/delete/<str:pk>/', views.delete_fixture, name='delete-fixture'),
    
    path('tournaments-create/', views.create_tournament, name='create-tournament'),
    path('tournaments/edit/<str:pk>/', views.edit_tournament, name='edit-tournament'),
    path('tournaments/delete/<str:pk>/', views.delete_tournament, name='delete-tournament'),

    path('ticket/buy/completed/<str:pk>', views.completed, name='completed'),
    path('ticket/buy/finished', views.finished, name='finished')
]
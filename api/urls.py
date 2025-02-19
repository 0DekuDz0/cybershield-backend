from django.contrib import admin
from django.urls import include, path
from api import views

urlpatterns = [
    path('get_participant_all/', views.get_participants),
    path('get_participant_by_id/', views.get_participant_by_id),
    path('get_participant_by_name/', views.get_participants_by_name),
    path('get_participant_by_email/', views.get_participant_by_email),
    path('get_participant_by_status/', views.get_participants_by_status),
    path('get_participant_by_team/', views.get_participants_by_team),
    path('add_participant/', views.add_participant),
    path('update_participant/', views.update_participant),
    path('delete_participant/', views.delete_participant),
    path('get_team_all/', views.get_teams),
    path('get_team_by_id/', views.get_team_by_id),
    path('get_team_by_name/', views.get_teams_by_name),
    path('add_team/', views.add_team),
    path('update_team/', views.update_team),
    path('delete_team/', views.delete_team),
    path('login/', views.login),
    
]

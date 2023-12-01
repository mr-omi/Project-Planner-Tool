from django.urls import path
from team_project_planner.managers.Team import *

urlpatterns = [
    path('', get_teams),
    path('create/', create_team, name="create_team"),
    path('describe/', describe_team, name="describe_team"),
    path('update/', update_team, name="update_team"),
    path('add_users/', add_new_users, name="add_new_users"),
    path('remove_users/', remove_users, name="remove_users"),
    path('list_users/', list_team_users, name="list_team_users")
]

from django.urls import path
from team_project_planner.managers.User import *

urlpatterns = [
    path('', get_users),
    path('create/', create_user, name="create_user"),
    path('describe/', describe_user, name="describe_user"),
    path('update/', update_user, name="update_user"),
    path('get_teams/', get_user_teams, name="get_teams")
]

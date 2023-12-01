from django.urls import include, path
from team_project_planner import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', include('team_project_planner.routes.User')),
    path('teams/', include('team_project_planner.routes.Team')),
    path('boards/', include('team_project_planner.routes.Board'))
]

from django.urls import path
from team_project_planner.managers.Board import *

urlpatterns = [
    path('create/', create_board, name='create_board'),
    path('close/', close_board, name="close_board"),
    path('add_task/', add_task, name="add_task"),
    path('update_task/', update_task_status, name="update_task_status"),
    path('list_boards/', list_boards, name="list_boards"),
    path('list_tasks/', list_tasks, name="list_tasks"),
    path('export/', export_board, name="export")
]

import os
from .models import *

output_path = os.getcwd()+"\out"


def write_board_to_out(board: Board):
    board_id = board.id
    board_name = board.name
    board_description = board.description
    board_created = board.created_at
    board_updated = board.updated_at
    tasks = Task.objects.filter(board_id=board_id)
    text_file_path = output_path + f"\\{board_name}_{board_id}.txt"
    # text_file_path = text_file_path.replace(" ", "_")
    with open(text_file_path, "w") as f:
        f.write("")
        f.close()
    with open(text_file_path, "a") as f:
        f.write(f"Welcome to Board {board_name}\n")
        f.write("\nid: " + str(board_id))
        f.write("\ndescription: " + board_description)
        f.write("\nTeam responsible: " + board.team.name)
        f.write("\nTeam admin: " + board.team.admin.name)
        if tasks.exists():
            f.write("\n\n\nHere's a list of the tasks:")
        for task in tasks:
            user = User.objects.get(id=task.user.id)
            f.write(
                f"\n    Task ID: {task.id}\n    Task Title: {task.title}\n    Task Description: {task.description}\n    To be done by: {user.name}\n    Task Status: {task.status}\n")
        f.write(f"\n\n\nBoard created at: {board_created}.\nLast Updated: {board_updated}")
        f.close()

    return text_file_path

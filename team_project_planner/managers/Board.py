from django.db.models import Q
from django.http import JsonResponse
from team_project_planner.helper import *
from team_project_planner.models import *
from team_project_planner.writer import *


@csrf_exempt
def create_board(request):
    body = json.loads(request.body)
    name = body.get("name")
    description = body.get("description")
    team_id = body.get("team_id")
    filtered_board = Board.objects.filter(Q(team=team_id) & Q(name=name))

    time = timezone.now()
    if filtered_board.exists():
        if filtered_board.filter(status="OPEN").exists():
            return JsonResponse({"error": f"Open board with name {name} already exists for team {team_id}"})
        else:
            board = filtered_board[0]
            board.status = "OPEN"
            board.updated_at = time
            board.save()
            return JsonResponse(
                {"Notice": f"Previously closed board with name {name} of team {team_id} is now re-opened"})

    team = Team.objects.get(id=team_id)

    board = Board(
        name=name,
        team=team,
        description=description,
        created_at=time,
        updated_at=time
    )
    board.save()
    return JsonResponse({"id": board.id}, safe=False)


@csrf_exempt
def close_board(request):
    body = json.loads(request.body)
    id = body.get("id")
    board = Board.objects.get(id=id)
    if board.status == "OPEN":
        for task in Task.objects.filter(board=id):
            if task.status != "COMPLETE":
                return JsonResponse({"error": f"task with title {task.title} has not been completed"})
        board.status = 'CLOSED'
        board.save()
    else:
        return JsonResponse({"status": "Already closed"})
    return JsonResponse({"status": board.status})


@csrf_exempt
def add_task(request):
    body = json.loads(request.body)
    title = body.get("title")
    board_id = body.get("board_id")
    description = body.get("description")
    user_id = body.get("user_id")

    board = Board.objects.get(id=board_id)
    team = board.team
    if (user_id not in team.users) and (user_id != team.admin.id):
        return JsonResponse({"error": f"Sorry, task can be assigned only to users of board {board.name}."})

    if board.status == "CLOSED":
        return JsonResponse({"error": "Sorry, task can be added only to an open board."})

    if Task.objects.filter(Q(title=title) & Q(board=board_id)):
        return JsonResponse({"error": f"Task with title {title} already exists on this board"})

    user = User.objects.get(id=user_id)
    time = timezone.now()
    task = Task(
        title=title,
        board=board,
        description=description,
        user=user,
        created_at=time,
        updated_at=time
    )
    task.save()
    return JsonResponse({"id": task.id}, safe=False)

    pass


@csrf_exempt
def update_task_status(request):
    body = json.loads(request.body)
    id = body.get("id")
    new_status = body.get("status")
    task = Task.objects.get(id=id)
    time = timezone.now()
    if new_status not in task_status_options:
        return JsonResponse({"error": f"Invalid update provided. New status must be one of {task_status_options}"})
    task.status = new_status
    task.updated_at = time
    task.save()
    return JsonResponse({"Success": f"status of task {task.title} updated to {new_status}"})


@csrf_exempt
def list_boards(request):
    body = json.loads(request.body)
    team_id = body.get("id")
    res = [{"id": board.id,
            "name": board.name,
            }
           for board in Board.objects.filter(team_id=team_id)]
    return JsonResponse(res, safe=False)


@csrf_exempt
def list_tasks(request):
    body = json.loads(request.body)
    team_id = body.get("id")
    boards = Board.objects.filter(team_id=team_id)
    tasks = []
    for board in boards:
        res = {"Board Name": board.name, "Task": [{" Title": task.title,
                                                   "Status": task.status} for task in
                                                  Task.objects.filter(board=board.id)]}
        tasks.append(res)

    return JsonResponse(tasks, safe=False)


@csrf_exempt
def export_board(request):
    body = json.loads(request.body)
    id = body.get("id")
    board = Board.objects.get(id=id)
    res = write_board_to_out(board=board)

    return JsonResponse({"filepath": res})

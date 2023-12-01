from django.http import JsonResponse
from team_project_planner.helper import *
from team_project_planner.models import *


def get_teams(request):
    teams = Team.objects.all()
    json_data = []
    for team in teams:
        json_data.append({
            "name": team.name,
            "description": team.description,
            "admin": team.admin.id,
            "users": team.users,
            "created_at": team.created_at
        })

    return JsonResponse(json_data, safe=False)


@csrf_exempt
def create_team(request):
    body = json.loads(request.body)
    name = body.get("name")
    admin_id = body.get("admin")
    description = body.get("description")
    users = body.get("users") if body.get("users") else []

    if Team.objects.filter(name=name).exists():
        return JsonResponse({"error": f"team with name {name} already exists"})

    admin = User.objects.get(id=admin_id)
    time = timezone.now()
    team = Team(
        name=name,
        admin=admin,
        description=description,
        users=users,
        created_at=time,
        updated_at=time
    )
    team.save()

    return JsonResponse({"id": team.id}, safe=False)


@csrf_exempt
def describe_team(request):
    body = json.loads(request.body)
    id = body.get("id")
    team = Team.objects.get(id=id)
    res = {
        "name": team.name,
        "description": team.description,
        "admin": team.admin.id,
        "created_at": team.created_at
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def update_team(request):
    body = json.loads(request.body)
    id = body.get("id")
    updates = body.get("team")
    time = timezone.now()
    updates["updated_at"] = time
    team = Team.objects.filter(id=id)
    team.update(**updates)
    team = Team.objects.get(id=id)
    res = {
        "name": team.name,
        "admin": team.admin.id,
        "description": team.description,
        "created_at": team.created_at,
        "updated_at": team.updated_at
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def add_new_users(request):
    body = json.loads(request.body)
    id = body.get("id")
    new_users = body.get("users")
    new_users = [user["id"] for user in User.objects.filter(id__in=new_users).values('id')]
    team = Team.objects.get(id=id)
    admin_id = team.admin.id
    current_users = team.users
    if len(current_users) + len(new_users) > 50:
        return JsonResponse({"Error": "Number of users after addition exceeds 50. Kindly reduce new users"})
    for new_user in new_users:
        if new_user not in current_users and new_user != admin_id:
            team.users.append(new_user)
    team.save()
    res = {
        "name": team.name,
        "admin": team.admin.id,
        "description": team.description,
        "users": team.users,
        "created_at": team.created_at,
        "updated_at": team.updated_at
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def remove_users(request):
    body = json.loads(request.body)
    id = body.get("id")
    old_users = body.get("users")
    old_users = [user["id"] for user in User.objects.filter(id__in=old_users).values('id')]
    team = Team.objects.get(id=id)
    admin_id = team.admin.id
    current_users = team.users
    for user_index in range(len(current_users) - 1, -1, -1):
        current_user = current_users[user_index]
        if current_user in old_users:
            team.users.pop(user_index)
    team.save()
    res = {
        "name": team.name,
        "admin": team.admin.id,
        "description": team.description,
        "users": team.users,
        "created_at": team.created_at,
        "updated_at": team.updated_at
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def list_team_users(request):
    body = json.loads(request.body)
    id = body.get("id")
    team = Team.objects.get(id=id)
    admin = team.admin
    all_users = [admin]
    for user_id in team.users:
        all_users.append(User.objects.get(id=user_id))
    res = list(map(lambda x:
                   {"id": x.id,
                    "name": x.name,
                    "display_name": x.display_name,
                    "admin": bool(x == admin)},
                   all_users))
    return JsonResponse(res, safe=False)

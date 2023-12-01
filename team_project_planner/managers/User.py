from django.db.models import Q
from django.http import JsonResponse
from team_project_planner.helper import *
from team_project_planner.models import *


def get_users(request):
    users = User.objects.all()
    json_data = []
    for user in users:
        json_data.append({
            "name": user.name,
            "display_name": user.display_name,
            "description": user.description,
            "created_at": user.created_at
        })

    return JsonResponse(json_data, safe=False)


@csrf_exempt
def describe_user(request):
    body = json.loads(request.body)
    id = body.get("id")
    user = User.objects.get(id=id)
    res = {
        "name": user.name,
        "display_name": user.display_name,
        "description": user.description,
        "created_at": user.created_at
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def create_user(request):
    body = json.loads(request.body)
    name = body.get("name")
    display_name = body.get("display_name")
    description = body.get("description")

    if User.objects.filter(name=name).exists():
        return JsonResponse({"error": f"User with name {name} already exists"})

    time = timezone.now()
    user = User(
        name=name,
        display_name=display_name,
        description=description,
        created_at=time,
        updated_at=time
    )
    user.save()

    return JsonResponse({"id": user.id}, safe=False)


@csrf_exempt
def update_user(request):
    body = json.loads(request.body)
    id = body.get("id")
    updates = body.get("user")
    time = timezone.now()
    updates["updated_at"] = time
    if "name" in updates:
        updates.pop("name")
    user = User.objects.filter(id=id)
    user.update(**updates)
    user = User.objects.get(id=id)
    res = {
        "name": user.name,
        "display_name": user.display_name,
        "description": user.description,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    return JsonResponse(res, safe=False)


@csrf_exempt
def get_user_teams(request):
    body = json.loads(request.body)
    user_id = body.get("id")
    teams = Team.objects.filter(
        Q(users__contains=[user_id]) | Q(admin_id=user_id)
    ).values("name", "description", "created_at")
    res = [team for team in teams]
    return JsonResponse(res, safe=False)

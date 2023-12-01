from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    users = ArrayField(models.IntegerField(), blank=True, null=True)

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class Board(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, max_length=128)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        choices=[("OPEN", "Open"), ("CLOSED", "Closed")],
        default="OPEN",
    )

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = (("team", "name"),)


class Task(models.Model):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        choices=[("OPEN", "Open"), ("IN_PROGRESS", "In Progress"), ("COMPLETE", "Complete")],
        default="OPEN",
    )

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = (("board", "title"),)

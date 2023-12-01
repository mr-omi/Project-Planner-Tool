import json
import os
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


task_status_options = ["OPEN", "IN_PROGRESS", "COMPLETE"]

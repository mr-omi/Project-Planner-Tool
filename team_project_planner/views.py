from django.http import HttpResponse

def home(response):
    return HttpResponse("<h1 style='text-align: center'>Home Page</h1>")

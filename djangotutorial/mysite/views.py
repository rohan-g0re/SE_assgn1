from django.http import HttpResponse


def home(request):
    return HttpResponse("Django Tutorial App is running. Go to /polls/ to vote.")

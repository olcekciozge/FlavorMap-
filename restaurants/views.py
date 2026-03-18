from django.http import HttpResponse


def index(request):
    return HttpResponse("100 aldıracak başarılı bir proje)")
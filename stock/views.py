from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse(" Stock has the high return")

def about(request):
    return HttpResponse("Stock says here is some information about this app")
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    context_dict = {'boldmessage':'hi,julia'}
    return render(request,'stock/index.html', context=context_dict)

def about(request):
    return render(request,'stock/about.html')
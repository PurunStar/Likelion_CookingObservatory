from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')

def intro(request) :
    return render(request, 'intro.html')

def notice(request) :
    return render(request, 'notice.html')
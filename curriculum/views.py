from django.shortcuts import render

# Create your views here.

def curi1(request):
    return render(request, 'curi1.html')




def curr_landing_page(request):
    return render(request, 'curr_landing_page.html')


def landing_page(request):
    return render(request, 'landing_page.html')

def lv1List(request):
    return render(request, 'lv1List.html')

def timer(request):
    return render(request, 'timer.html')
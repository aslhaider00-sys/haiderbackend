# from django.http import HttpResponse
from django.shortcuts import render
def homepage(request):
    # return HttpResponse("Hey, it's me Goku.")
    return render(request, 'home.html')
def about(request):
    # return HttpResponse("My Page")
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def donate(request):
    return render(request, 'donate.html')
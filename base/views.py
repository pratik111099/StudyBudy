from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homeView(request):
    return HttpResponse('Home page')

def roomView(request):
    return HttpResponse('Room page')

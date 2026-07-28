from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse('Página de login')

def forgot_password(request):
    return HttpResponse('Página de recuperação de senha')
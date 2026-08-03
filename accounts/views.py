from django.shortcuts import render
from django.http import HttpResponse

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')

    elif request.method == 'POST':
            email = request.POST.get('email')
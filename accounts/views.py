from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Search for the user by the registered email (or if the email was used in the username field)
        user_obj = User.objects.filter(email=email).first() or User.objects.filter(username=email).first()
        
        if user_obj:
            # Authenticates the password using the corresponding username.
            user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)      # Creates the session for the logged-in user.
                return redirect('home')   # Redirects to the route named 'home'
        
        # If the credentials are incorrect
        return render(request, 'login.html', {'error': 'E-mail ou senha inválidos'})

def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'forgot_password.html')

    elif request.method == 'POST':
            email = request.POST.get('email')
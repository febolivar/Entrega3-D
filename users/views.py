""" View's module for User's Apps"""

# Django

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Forms 

from users.forms import SignupForm

# Test
from django.http import HttpResponse

# View's methods start

def login_view(request):
    """ Login view method """
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            return render(request, 'users/login.html', {'error': 'Nombre de usuario o contraseña no valido'})

    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    """ Logout view method """
    logout(request)
    return redirect('home:home')


def signup(request):
    """ Signup view method """
    #if(request.method == 'POST'):
    #    print(request.POST)
    #    if 'is_enterprise' in request.POST:
    #        print(request.POST['is_enterprise'])

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = SignupForm()
    
    return render(request = request, 
        template_name = 'users/signup.html',
        context = {'form': form })



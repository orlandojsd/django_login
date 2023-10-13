from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserUpdateForm, UserRegistrationForm 
from django.http import HttpResponse


@login_required
def index(request):
    """
    This view renders the index

    enders index.html and sends the user arguments.
    """
    return render (request, 'index.html', {'user': request.user})
    
def user_login(request):
    """
    This view is used to log in a user

    If the request method is post, the information is validated with a form, 
    login is done and it is redirected to the view index. Otherwise, login is required.
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    """
    This view used to log out

    The django logout method is called and redirected to the login view.
    """
    logout(request)
    return redirect('login')

@login_required
def update_user(request):
    """
    This view is used to update a user

    If the request method is post, the information is validated with a form, 
    update is done and render to template update_confirmation. 
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save() #if form is valid user will be update
            return render(request, 'update_confirmation.html', {'user': request.user})
    else:
        print(request.user.last_name)
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update.html', {'form': form})


def registration_user(request):
    """
    This view is used to register a user

    If the request method is post, the information is validated with a form, 
    update is done and it is redirected to the view index.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() #if form is valid user save. 
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

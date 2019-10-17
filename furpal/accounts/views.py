from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib import messages

from .forms import LoginForm, RegisterForm


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    redirect_path = 'furpal-home'
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                messages.success(request, f'Your login is successful')
                return redirect(redirect_path)
            else:
                messages.failure(request, f'Your login is unsuccessful, check if you entered your email and password correctly')
                return redirect("/")
        else:
            messages.success(request, f'Your login is unsuccessful, check if you entered your email and password correctly.')
    return render(request, "accounts/login.html", context)


User = get_user_model()


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

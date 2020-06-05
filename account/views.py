from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404, redirect

from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index-page')
    
    form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


class LogoutView():
    pass
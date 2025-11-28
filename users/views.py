from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from exchange.models import Balance

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Balance.objects.create(user=user, coins=50)  # bonus inscription
            return redirect('exchange:home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

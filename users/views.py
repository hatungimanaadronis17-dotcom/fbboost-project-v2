from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from exchange.models import Balance


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Bonus de 50 coins à l’inscription
            Balance.objects.get_or_create(user=user, defaults={'coins': 50})
            messages.success(request, 'Inscription réussie ! Tu reçois 50 coins gratuits.')
            return redirect('exchange:home')   # ← C’EST ÇA QUI MANQUAIT
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    # Récupère le solde de l’utilisateur
    balance = Balance.objects.get(user=request.user)
    return render(request, 'users/profile.html', {'balance': balance})

# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Le signal dans exchange/signals.py crée automatiquement la Balance avec 50 coins
            # Pas besoin de le faire ici

            login(request, user)  # Connexion automatique après inscription
            messages.success(request, 'Inscription réussie ! Tu gagnes 50 coins gratuits.')
            return redirect('exchange:home')  # Redirection vers la page d'échange
        else:
            messages.error(request, 'Erreur dans le formulaire. Vérifie les champs.')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # Récupère la Balance (grâce au signal, elle existe toujours)
    balance = getattr(request.user, 'balance', None)
    
    return render(request, 'users/profile.html', {
        'balance': balance
    })

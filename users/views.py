# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login  # Pour connecter automatiquement après inscription

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crédite 50 coins à l'inscription (si tu as un modèle Balance)
            try:
                from exchange.models import Balance
                Balance.objects.create(user=user, coins=50)
            except:
                pass  # Si Balance n'existe pas encore, ignore

            messages.success(request, 'Inscription réussie ! Tu gagnes 50 coins gratuits. Tu es maintenant connecté.')
            login(request, user)  # Connecte automatiquement l'utilisateur
            return redirect('exchange:home')  # ou '/' ou la page que tu veux
        else:
            messages.error(request, 'Erreur dans le formulaire. Vérifie les champs.')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

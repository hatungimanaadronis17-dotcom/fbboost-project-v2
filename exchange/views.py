# exchange/views.py – Version finale corrigée (prête à coller)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
import re

from .models import Balance, Task


@login_required(login_url='/login/')
def exchange_home(request):
    # Protection anti-next infinie (tu l’as bien fait)
    if "next" in request.GET:
        dangerous_next = request.GET.get("next", "")
        if len(dangerous_next) > 400 or dangerous_next.count("/exchange") > 5:
            return redirect('exchange:exchange_home')

    # ON PASSE L'OBJET BALANCE, PAS JUSTE LE NOMBRE
    balance, _ = Balance.objects.get_or_create(user=request.user, defaults={'coins': 0})

    return render(request, 'exchange/home.html', {
        'balance': balance  # ← CORRIGÉ : objet complet
    })


@login_required(login_url='/login/')
def submit_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform', '').strip().lower()

    if not url or not platform:
        return JsonResponse({'error': 'URL et plateforme manquantes'}, status=400)

    if platform not in ['facebook', 'instagram', 'tiktok', 'youtube']:
        return JsonResponse({'error': 'Plateforme invalide'}, status=400)

    # Vérification basique que l'URL ressemble à quelque chose
    if not re.match(r'^https?://', url):
        return JsonResponse({'error': 'URL invalide (doit commencer par http ou https)'}, status=400)

    # Anti-triche : 1 tâche toutes les 90 secondes
    limit = timezone.now() - timedelta(seconds=90)
    if Task.objects.filter(user=request.user, created_at__gte=limit).exists():
        return JsonResponse({
            'error': 'Attends 90 secondes entre chaque tâche !',
            'cooldown': True
        }, status=429)

    # Récompense selon plateforme (comme Addmefast)
    rewards = {
        'facebook': 10,
        'instagram': 12,
        'tiktok': 15,
        'youtube': 20,
    }
    reward = rewards.get(platform, 10)

    # Création tâche + ajout coins
    Task.objects.create(
        user=request.user,
        platform=platform,
        url=url,
        validated=True,      # ou False si tu veux modération manuelle plus tard
        completed=True
    )

    balance = Balance.objects.get(user=request.user)
    balance.coins += reward
    balance.save()

    return JsonResponse({
        'success': True,
        'coins': reward,           # ← pour le +X coins
        'total': balance.coins,    # ← pour mise à jour live
        'message': f'+{reward} coins !'
    })

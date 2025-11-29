# exchange/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from .models import Balance, Task  # ajuste si tes modèles sont ailleurs


@login_required(login_url='/login/')
def exchange_home(request):
    # PROTECTION FORTE CONTRE L'ATTAQUE next= infinie
    if "next" in request.GET:
        dangerous_next = request.GET["next"]
        if len(dangerous_next) > 400 or dangerous_next.count("/exchange") > 5:
            # On redirige proprement sans planter
            return redirect('exchange_home')  # 'exchange_home' = le name de ton url

    # Récupération du solde de l'utilisateur
    balance, _ = Balance.objects.get_or_create(user=request.user)
    
    context = {
        'balance': balance.coins,
    }

    return render(request, 'exchange/home.html', context)


@login_required(login_url='/login/')
def submit_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST requis'}, status=400)

    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform', '').strip()

    if not url or not platform:
        return JsonResponse({'error': 'URL et plateforme requis'}, status=400)

    # Anti-triche : 1 tâche toutes les 90 secondes minimum
    ninety_seconds_ago = timezone.now() - timedelta(seconds=90)
    recent_task = Task.objects.filter(
        user=request.user,
        created_at__gte=ninety_seconds_ago
    ).exists()

    if recent_task:
        return JsonResponse({
            'error': 'Attends 90 secondes entre chaque tâche !',
            'cooldown': True
        }, status=429)

    # Création de la tâche
    task = Task.objects.create(
        user=request.user,
        platform=platform,
        url=url,
        validated=True,           # ou False si tu veux valider manuellement
        completed=True
    )
    task.save()

    # Ajout des coins
    balance = Balance.objects.get(user=request.user)
    reward = 10  # change selon ta logique
    balance.coins += reward
    balance.save()

    return JsonResponse({
        'success': True,
        'message': f'+{reward} coins !',
        'total': balance.coins,
        'new_balance': balance.coins
    })


# Ligne magique qui fait tout fonctionner
home = exchange_home

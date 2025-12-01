from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import re

from .models import Balance, Task


@login_required(login_url='/login/')
def home(request):                                            # ← C'EST LE BON NOM
    # Protection anti-next infinie
    if "next" in request.GET:
        dangerous_next = request.GET.get("next", "")
        if len(dangerous_next) > 400 or dangerous_next.count("/exchange") > 5:
            return redirect('exchange:home')

    balance, _ = Balance.objects.get_or_create(user=request.user, defaults={'coins': 0})

    return render(request, 'exchange/home.html', {
        'balance': balance
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

    if not re.match(r'^https?://', url):
        return JsonResponse({'error': 'URL invalide'}, status=400)

    # Anti-triche 90 secondes
    limit = timezone.now() - timedelta(seconds=90)
    if Task.objects.filter(user=request.user, created_at__gte=limit).exists():
        return JsonResponse({
            'error': 'Attends 90 secondes entre chaque tâche !',
            'cooldown': True
        }, status=429)

    # Récompenses comme Addmefast
    rewards = {'facebook': 10, 'instagram': 12, 'tiktok': 15, 'youtube': 20}
    reward = rewards.get(platform, 10)

    Task.objects.create(
        user=request.user,
        platform=platform,
        url=url,
        validated=True,
        completed=True
    )

    balance = Balance.objects.get(user=request.user)
    balance.coins += reward
    balance.save()

    return JsonResponse({
        'success': True,
        'coins': reward,
        'total': balance.coins,
        'message': f'+{reward} coins !'
    })

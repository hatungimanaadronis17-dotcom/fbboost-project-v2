from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import timedelta
import re

from .models import Balance, Task


@login_required(login_url='/accounts/login/')
def home(request):
    """Page d'accueil de l'échange (affiche le solde)"""
    balance, _ = Balance.objects.get_or_create(user=request.user, defaults={'coins': 0})
    return render(request, 'exchange/home.html', {
        'balance': balance
    })


# VUE CRUCIALE POUR TON APPLI ANDROID
@csrf_exempt  # Ton appli mobile n'envoie pas le token CSRF
@require_http_methods(["GET"])
def gagner_coins(request):
    """
    URL appelée par l'app Android quand l'utilisateur clique sur "Gagner des coins"
    Exemple : /gagner-coins/?url=https://www.tiktok.com/@user
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentification requise'}, status=401)

    url = request.GET.get('url', '').strip()
    if not url:
        return JsonResponse({'error': 'Paramètre url manquant'}, status=400)

    # Sécurité basique anti-spam (1 tâche toutes les 85 secondes)
    limit = timezone.now() - timedelta(seconds=85)
    recent = Task.objects.filter(user=request.user, created_at__gte=limit).exists()
    if recent:
        return JsonResponse({
            'error': 'Attends un peu avant la prochaine tâche',
            'cooldown': True
        }, status=429)

    # Détection simple de la plateforme via l'URL
    platform = 'autre'
    if 'tiktok.com' in url:
        platform = 'tiktok'
        reward = 15
    elif 'instagram.com' in url:
        platform = 'instagram'
        reward = 12
    elif 'facebook.com' in url or 'fb.me' in url:
        platform = 'facebook'
        reward = 10
    elif 'youtube.com' in url or 'youtu.be' in url:
        platform = 'youtube'
        reward = 20
    else:
        reward = 8  # plateforme inconnue mais on donne quand même un peu

    # Création de la tâche
    Task.objects.create(
        user=request.user,
        platform=platform,
        url=url,
        validated=True,
        completed=True
    )

    # Ajout des coins
    balance = Balance.objects.get(user=request.user)
    balance.coins += reward
    balance.save()

    return JsonResponse({
        'success': True,
        'coins_added': reward,
        'total_coins': balance.coins,
        'platform': platform,
        'message': f'+{reward} coins gagnés !'
    })


@login_required(login_url='/accounts/login/')
@csrf_exempt
@require_http_methods(["POST"])
def submit_task(request):
    """Permet de soumettre une tâche manuellement depuis le site web"""
    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform', '').strip().lower()

    if not url or not platform:
        return JsonResponse({'error': 'URL et plateforme requises'}, status=400)

    if platform not in ['facebook', 'instagram', 'tiktok', 'youtube']:
        return JsonResponse({'error': 'Plateforme invalide'}, status=400)

    if not re.match(r'^https?://', url, re.IGNORECASE):
        return JsonResponse({'error': 'URL invalide'}, status=400)

    # Anti-spam 90 secondes
    limit = timezone.now() - timedelta(seconds=90)
    if Task.objects.filter(user=request.user, created_at__gte=limit).exists():
        return JsonResponse({'error': 'Attends 90 secondes', 'cooldown': True}, status=429)

    rewards = {'facebook': 10, 'instagram': 12, 'tiktok':15, 'youtube':20}
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

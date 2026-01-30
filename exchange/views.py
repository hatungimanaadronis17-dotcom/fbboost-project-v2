from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from django.db import transaction
from datetime import timedelta
import uuid
import re

from .models import Balance, Task, Transaction


@login_required(login_url='/accounts/login/')
def home(request):
    """Page d'accueil de l'échange (affiche le solde et les tâches disponibles)"""
    balance, _ = Balance.objects.get_or_create(user=request.user, defaults={'coins': 50})
    
    # Tâches disponibles non complétées pour cet utilisateur
    pending_tasks = Task.objects.filter(user=request.user, completed=False).order_by('created_at')
    
    context = {
        'balance': balance,
        'pending_tasks': pending_tasks,
        'has_tasks': pending_tasks.exists(),
    }
    return render(request, 'exchange/home.html', context)


@login_required
def start_task(request, task_id):
    """
    Affiche la page de la tâche avec le bouton "Ouvrir la page"
    """
    task = get_object_or_404(Task, id=task_id, user=request.user, completed=False)

    # Génère un token unique pour cette tentative de vérification
    token = uuid.uuid4().hex
    task.verification_token = token
    task.last_verification_attempt = timezone.now()
    task.save(update_fields=['verification_token', 'last_verification_attempt'])

    context = {
        'task': task,
        'verification_token': token,
        'min_seconds': 5,
    }
    return render(request, 'exchange/task_start.html', context)


@require_POST
@login_required
def confirm_task(request):
    """
    Endpoint appelé quand l'utilisateur clique "J'ai terminé"
    Crédite automatiquement après vérification client-side
    """
    data = request.POST
    task_id = data.get('task_id')
    token = data.get('token')

    if not task_id or not token:
        return JsonResponse({'success': False, 'error': 'Données manquantes'}, status=400)

    try:
        task = Task.objects.get(
            id=task_id,
            user=request.user,
            verification_token=token,
            completed=False
        )
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tâche invalide, token expiré ou déjà terminée'}, status=400)

    with transaction.atomic():
        task.completed = True
        task.completed_at = timezone.now()
        task.verification_token = None
        task.save(update_fields=['completed', 'completed_at', 'verification_token'])

        balance = Balance.objects.select_for_update().get(user=request.user)
        balance.coins += task.coins_reward
        balance.save(update_fields=['coins', 'updated_at'])

        Transaction.objects.create(
            user=request.user,
            tx_type='credit',
            coins=task.coins_reward,
            description=f"{task.platform} {task.action} confirmé après vérification"
        )

    # Trouve la prochaine tâche non complétée
    next_task = Task.objects.filter(user=request.user, completed=False).first()

    response = {
        'success': True,
        'coins_added': task.coins_reward,
        'total_coins': balance.coins,
        'message': f"+{task.coins_reward} coins ajoutés !",
    }

    if next_task:
        response['next_task_url'] = f"/exchange/task/{next_task.id}/"
        response['next_message'] = "Prochaine tâche disponible !"
    else:
        response['next_message'] = "Toutes les tâches sont terminées pour le moment."

    return JsonResponse(response)


# Soumission AJAX du site web
@csrf_exempt
@require_http_methods(["POST"])
def submit_task(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentification requise'}, status=401)

    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform', '').strip().lower()

    if not url or not platform:
        return JsonResponse({'error': 'URL et plateforme requises'}, status=400)

    if platform not in ['facebook', 'instagram', 'tiktok', 'youtube']:
        return JsonResponse({'error': 'Plateforme invalide'}, status=400)

    if not re.match(r'^https?://', url, re.IGNORECASE):
        return JsonResponse({'error': 'URL invalide'}, status=400)

    limit = timezone.now() - timedelta(seconds=90)
    if Task.objects.filter(user=request.user, created_at__gte=limit).exists():
        return JsonResponse({'error': 'Attends 90 secondes avant la prochaine tâche', 'cooldown': True}, status=429)

    rewards = {'facebook': 10, 'instagram': 12, 'tiktok': 15, 'youtube': 20}
    reward = rewards.get(platform, 10)

    Task.objects.create(
        user=request.user,
        platform=platform,
        task_url=url,
        coins_reward=reward,
        completed=False,
        validated=False
    )

    return JsonResponse({
        'success': True,
        'message': f'Tâche créée – complète-la pour gagner {reward} coins'
    })


# Pour l'app Android
@csrf_exempt
@require_http_methods(["GET"])
def gagner_coins(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentification requise'}, status=401)

    url = request.GET.get('url', '').strip()
    if not url:
        return JsonResponse({'error': 'Paramètre url manquant'}, status=400)

    limit = timezone.now() - timedelta(seconds=85)
    if Task.objects.filter(user=request.user, created_at__gte=limit).exists():
        return JsonResponse({'error': 'Attends un peu avant la prochaine tâche', 'cooldown': True}, status=429)

    platform = 'autre'
    reward = 8

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

    Task.objects.create(
        user=request.user,
        platform=platform,
        task_url=url,
        coins_reward=reward,
        completed=False,
        validated=False
    )

    return JsonResponse({
        'success': True,
        'coins_added': reward,
        'message': f'+{reward} coins gagnés ! (à confirmer)'
    })

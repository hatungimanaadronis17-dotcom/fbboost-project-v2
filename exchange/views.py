from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
import uuid

from .models import Balance, Task, Transaction


@login_required
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
    task.verification_token = token  # Ajoute ce champ dans models.py si absent
    task.save(update_fields=['verification_token'])

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
    Vérifie le timer et crédite si conditions OK
    """
    data = request.POST  # ou json.loads(request.body) si AJAX
    task_id = data.get('task_id')
    token = data.get('token')

    try:
        task = Task.objects.get(
            id=task_id,
            user=request.user,
            verification_token=token,
            completed=False
        )
    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tâche invalide ou déjà terminée'}, status=400)

    # Ici : tu peux ajouter une vérification plus stricte si besoin
    # Pour l'instant : crédit automatique après le timer client-side

    with transaction.atomic():
        task.completed = True
        task.completed_at = timezone.now()
        task.verification_token = None  # Nettoie le token
        task.save()

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


# Endpoint JSON pour Android / API (optionnel, si tu as une app mobile)
@csrf_exempt
@require_POST
def api_submit_task(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentification requise'}, status=401)

    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform', '').lower()

    if not url or not platform:
        return JsonResponse({'error': 'URL et plateforme requises'}, status=400)

    # Vérification cooldown
    cooldown_time = timezone.now() - timedelta(seconds=90)
    if Task.objects.filter(user=request.user, created_at__gte=cooldown_time).exists():
        return JsonResponse({'error': 'Attends 90 secondes avant la prochaine tâche'}, status=429)

    rewards = {'facebook': 10, 'instagram': 12, 'tiktok': 15, 'youtube': 20}
    reward = rewards.get(platform, 8)

    # Création de la tâche (mais pas crédit immédiat)
    task = Task.objects.create(
        user=request.user,
        platform=platform,
        task_url=url,
        coins_reward=reward,
        completed=False,
        validated=False
    )

    return JsonResponse({
        'success': True,
        'task_id': task.id,
        'message': f"Tâche créée – complète-la pour gagner {reward} coins",
        'redirect_to': f"/exchange/task/{task.id}/"  # ou ton URL mobile
    })

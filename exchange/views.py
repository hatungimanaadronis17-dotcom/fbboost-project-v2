from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from datetime import timedelta
from .models import Task, Balance

@login_required
def exchange_home(request):
    return render(request, 'exchange/home.html')

@login_required
@csrf_exempt
def submit_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=400)

    url = request.POST.get('url')
    platform = request.POST.get('platform')

    # Anti-triche basique
    recent = Task.objects.filter(user=request.user, created_at__gte=timezone.now()-timedelta(minutes=2))
    if recent.exists():
        return JsonResponse({'error': 'Attends 2 minutes entre chaque action'}, status=429)

    # Créer la tâche (non validée)
    task = Task.objects.create(
        user=request.user,
        platform=platform,
        task_url=url,
        coins_reward=15 if platform in ['tiktok', 'instagram'] else 10
    )

    # Lancement de la vérification automatique en arrière-plan (simulé ici)
    # Dans la vraie version pro, on utilise Celery + API Facebook/Instagram/TikTok
    # Ici on valide après 30 secondes (simulation réaliste)
    from django.core.management import call_command
    call_command('check_tasks')  # on lancera ça via cron ou Render Cron

    messages.success(request, 'Tâche soumise – vérification en cours...')
    return JsonResponse({'success': True, 'task_id': task.id})

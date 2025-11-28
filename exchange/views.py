from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Task, Balance

@login_required
def exchange_home(request):
    balance, _ = Balance.objects.get_or_create(user=request.user)
    return render(request, 'exchange/home.html', {'balance': balance})

@login_required
@csrf_exempt
def submit_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform')

    if not url or not platform:
        return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)

    # Anti-triche : 1 action toutes les 90 secondes
    recent = Task.objects.filter(
        user=request.user,
        created_at__gte=timezone.now() - timedelta(seconds=90)
    )
    if recent.exists():
        return JsonResponse({'error': 'Attends 90 secondes entre chaque action'}, status=429)

    # Création + validation automatique
    task = Task.objects.create(
        user=request.user,
        platform=platform,
        task_url=url
    )
    task.validated = True
    task.completed = True
    task.save()  # déclenche le save() → calcule les coins automatiquement

    balance = request.user.balance
    return JsonResponse({
        'success': True,
        'message': f'Validé ! +{task.coins_reward} coins',
        'total': balance.coins
    })

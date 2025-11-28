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
        return JsonResponse({'error': 'POST requis'}, status=400)

    url = request.POST.get('url', '').strip()
    platform = request.POST.get('platform')

    # Anti-triche 90s
    if Task.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(seconds=90)).exists():
        return JsonResponse({'error': 'Attends 90 secondes'}, status=429)

    task = Task.objects.create(user=request.user, platform=platform, task_url=url)
    task.validated = True
    task.completed = True
    task.save()  # déclenche le calcul des coins

    balance = Balance.objects.get(user=request.user)
    return JsonResponse({
        'success': True,
        'message': f'+{task.coins_reward} coins',
        'total': balance.coins
    })

# exchange/tasks.py (à exécuter avec un cron ou Render Background Worker)
from django.utils import timezone
from .models import Task, Balance
import time
import random

def check_and_validate_tasks():
    pending_tasks = Task.objects.filter(completed=False)
    for task in pending_tasks:
        # Simulation de vérification réelle (dans la vraie version : API Graph + screenshot)
        if random.choice([True, True, True, False]):  # 75% de succès
            task.completed = True
            task.validated = True
            task.save()

            balance, _ = Balance.objects.get_or_create(user=task.user)
            balance.coins += task.coins_reward
            balance.save()
            print(f"[AUTO] +{task.coins_reward} coins pour {task.user}")
        else:
            task.delete()  # tâche fausse supprimée
        time.sleep(1)

# exchange/migrations/0003_merge.py

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
        ('exchange', '0002_balance_task_withdrawal'),  # ← Adapte ce nom EXACTEMENT à celui que tu as (regarde ta capture : probablement 0002_balance_task_withdrawal)
    ]

    operations = [
        # Cette migration est vide : elle ne fait que fusionner les deux branches
    ]

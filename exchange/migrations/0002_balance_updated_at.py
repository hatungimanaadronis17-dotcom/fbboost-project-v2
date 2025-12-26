
# exchange/migrations/0002_balance_updated_at.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),  # Dépend de ta migration initiale qui a créé Balance, Task, Withdrawal
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, blank=True),
        ),
        # Optionnel mais recommandé : date de création
        migrations.AddField(
            model_name='balance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, blank=True),
        ),
    ]

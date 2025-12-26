# exchange/migrations/0002_balance_updated_at.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),  # Doit correspondre au nom de ta migration initiale
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, blank=True),
            preserve_default=False,
        ),
        # Optionnel mais fortement recommandé : ajouter created_at en même temps
        migrations.AddField(
            model_name='balance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, blank=True),
            preserve_default=False,
        ),
    ]

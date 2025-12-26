# exchange/migrations/0001_initial.py

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),  # Dépend de la migration initiale de l'app users
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coins', models.IntegerField(default=50)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Balance',
                'verbose_name_plural': 'Balances',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(
                    max_length=20,
                    choices=[
                        ('facebook', 'Facebook'),
                        ('instagram', 'Instagram'),
                        ('tiktok', 'TikTok'),
                        ('youtube', 'YouTube')
                    ]
                )),
                ('action', models.CharField(
                    max_length=20,
                    choices=[(a, a.capitalize()) for a in ['follow', 'subscribe', 'like', 'comment', 'abonne']]
                )),
                ('task_url', models.URLField(max_length=500)),
                ('coins_reward', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('validated', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tasks_done',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(
                    max_length=20,
                    choices=[
                        ('paypal', 'PayPal'),
                        ('interac', 'Interac e-Transfer'),
                        ('crypto', 'Crypto (USDT/BTC)'),
                    ]
                )),
                ('amount_cad', models.DecimalField(max_digits=10, decimal_places=2)),
                ('details', models.CharField(max_length=200)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Withdrawal',
                'verbose_name_plural': 'Withdrawals',
            },
        ),
    ]

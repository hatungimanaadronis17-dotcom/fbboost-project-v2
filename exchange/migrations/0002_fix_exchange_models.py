from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [

        # =========================
        # BALANCE
        # =========================

        migrations.AlterField(
            model_name='balance',
            name='coins',
            field=models.PositiveIntegerField(default=0),
        ),

        migrations.RemoveField(
            model_name='balance',
            name='created_at',
        ),

        # =========================
        # TRANSACTION (NOUVELLE TABLE)
        # =========================

        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tx_type', models.CharField(
                    max_length=20,
                    choices=[
                        ('credit', 'Credit'),
                        ('debit', 'Debit'),
                        ('withdrawal', 'Withdrawal'),
                        ('bonus', 'Bonus'),
                    ]
                )),
                ('coins', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='transactions',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),

        # =========================
        # TASK
        # =========================

        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tasks',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        # =========================
        # WITHDRAWAL
        # =========================

        migrations.AddField(
            model_name='withdrawal',
            name='coins_amount',
            field=models.PositiveIntegerField(default=0),
        ),

        migrations.RemoveField(
            model_name='withdrawal',
            name='details',
        ),

        migrations.AlterField(
            model_name='withdrawal',
            name='status',
            field=models.CharField(
                max_length=20,
                default='pending',
                choices=[
                    ('pending', 'Pending'),
                    ('paid', 'Paid'),
                    ('rejected', 'Rejected'),
                ]
            ),
        ),
    ]

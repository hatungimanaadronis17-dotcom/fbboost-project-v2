from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_boost', models.BooleanField(default=True)),
                ('boost_delay', models.IntegerField(default=30)),
                ('coins', models.IntegerField(default=0)),
                ('boosts', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

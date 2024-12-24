# Generated by Django 5.1.4 on 2024-12-24 02:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(choices=[('CS', 'CASH'), ('CD', 'CARD'), ('SV', 'SAVINGS')], max_length=2)),
                ('category', models.CharField(choices=[('SL', 'SALARY'), ('CD', 'CARD'), ('FL', 'FREELANCE')], max_length=2)),
                ('text', models.TextField(default='')),
                ('money', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.1.6 on 2024-05-23 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sorties', '0003_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupeAmis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupes_crees', to=settings.AUTH_USER_MODEL)),
                ('membres', models.ManyToManyField(related_name='groupes_amis', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Groupe',
        ),
    ]

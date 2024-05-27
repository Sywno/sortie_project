# Generated by Django 4.2.13 on 2024-05-26 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sorties', '0006_rename_content_message_contenu_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vient', models.BooleanField()),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SortieProposee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('lieu', models.CharField(max_length=100)),
                ('createur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('groupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sorties.groupeamis')),
                ('participants', models.ManyToManyField(related_name='sorties_participants', through='sorties.Participation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='participation',
            name='sortie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sorties.sortieproposee'),
        ),
    ]

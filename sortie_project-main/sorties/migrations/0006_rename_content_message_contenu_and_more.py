# Generated by Django 4.2.13 on 2024-05-23 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sorties', '0005_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='contenu',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='timestamp',
            new_name='date_envoye',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='utilisateur',
        ),
    ]
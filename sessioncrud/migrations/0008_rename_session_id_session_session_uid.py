# Generated by Django 5.1.1 on 2024-10-06 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sessioncrud', '0007_session_session_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='session_id',
            new_name='session_uid',
        ),
    ]

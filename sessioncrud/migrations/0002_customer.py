# Generated by Django 5.1.1 on 2024-10-03 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessioncrud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.PositiveIntegerField(unique=True)),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_mail', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=254)),
            ],
        ),
    ]

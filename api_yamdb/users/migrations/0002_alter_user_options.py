# Generated by Django 3.2 on 2025-02-11 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('role',)},
        ),
    ]

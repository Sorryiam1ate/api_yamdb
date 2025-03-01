# Generated by Django 4.2.17 on 2025-02-15 11:12

import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20250213_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('role',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[users.validators.validate_username, django.core.validators.RegexValidator(regex='^[\\w.@+-]+\\Z')], verbose_name='Имя'),
        ),
    ]

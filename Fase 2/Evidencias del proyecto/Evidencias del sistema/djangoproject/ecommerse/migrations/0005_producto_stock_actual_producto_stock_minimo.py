# Generated by Django 5.0.6 on 2024-11-14 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerse', '0004_alter_usuario_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock_actual',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='stock_minimo',
            field=models.PositiveIntegerField(default=10),
        ),
    ]

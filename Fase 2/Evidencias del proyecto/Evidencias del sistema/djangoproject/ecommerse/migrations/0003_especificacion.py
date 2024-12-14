# Generated by Django 5.0.6 on 2024-12-06 22:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerse', '0002_listadeseados'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristica', models.CharField(max_length=255)),
                ('detalle', models.CharField(max_length=255)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='especificaciones', to='ecommerse.producto')),
            ],
        ),
    ]
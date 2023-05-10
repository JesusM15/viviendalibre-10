# Generated by Django 4.2 on 2023-04-29 16:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inmuebles', '0003_plan_suscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='suscripcion',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]

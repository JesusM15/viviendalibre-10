# Generated by Django 4.2 on 2023-04-29 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='creditCardTokenId',
            field=models.TextField(blank=True),
        ),
    ]

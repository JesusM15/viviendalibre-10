# Generated by Django 4.2 on 2023-05-13 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_payer_id_paypal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telefono',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]

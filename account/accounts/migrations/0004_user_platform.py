# Generated by Django 5.0.7 on 2024-08-14 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_cities_state_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='platform',
            field=models.CharField(choices=[('email', 'Email'), ('google', 'Google'), ('facebook', 'Facebook')], default='email', max_length=20),
        ),
    ]

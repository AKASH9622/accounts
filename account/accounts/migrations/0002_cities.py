# Generated by Django 5.0.7 on 2024-07-18 14:39

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cities',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('flag', models.IntegerField(blank=True, default=1, verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('state_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.countries')),
            ],
            options={
                'db_table': 'cities',
            },
        ),
    ]

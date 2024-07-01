# Generated by Django 5.0.6 on 2024-07-01 00:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_post_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkedinUserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub', models.CharField(max_length=255)),
                ('name', models.TextField(blank=True)),
                ('given_name', models.CharField(blank=True, max_length=255)),
                ('family_name', models.CharField(blank=True, max_length=255)),
                ('picture', models.TextField(blank=True)),
                ('locale', models.CharField(blank=True, max_length=255)),
                ('email', models.CharField(blank=True, max_length=255)),
                ('email_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
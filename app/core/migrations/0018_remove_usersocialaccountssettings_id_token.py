# Generated by Django 5.0.6 on 2024-06-29 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_usersocialaccountssettings_id_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersocialaccountssettings',
            name='id_token',
        ),
    ]
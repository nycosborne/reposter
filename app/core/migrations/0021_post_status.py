# Generated by Django 5.0.6 on 2024-06-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_usersocialaccountssettings_id_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('IN_REVIEW', 'In Review'), ('PUBLISHED', 'Published')], default='DRAFT', max_length=10),
        ),
    ]

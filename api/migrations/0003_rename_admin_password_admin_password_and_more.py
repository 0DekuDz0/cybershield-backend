# Generated by Django 5.1.5 on 2025-02-18 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_participant_participant_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='admin_password',
            new_name='password',
        ),
        migrations.AddField(
            model_name='admin',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]

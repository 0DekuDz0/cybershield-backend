# Generated by Django 5.1.5 on 2025-02-16 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='participant_status',
            field=models.CharField(blank=True, default='Pending', max_length=20, null=True),
        ),
    ]

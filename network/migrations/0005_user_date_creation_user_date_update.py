# Generated by Django 4.0.3 on 2022-11-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

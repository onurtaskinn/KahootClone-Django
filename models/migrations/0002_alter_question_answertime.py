# Generated by Django 3.2.1 on 2023-04-14 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answerTime',
            field=models.IntegerField(default=10, null=True),
        ),
    ]

# Generated by Django 3.2.1 on 2023-05-08 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_alter_question_answertime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-id']},
        ),
    ]

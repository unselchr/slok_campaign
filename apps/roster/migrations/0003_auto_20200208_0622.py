# Generated by Django 3.0.2 on 2020-02-08 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0002_auto_20200208_0621'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='roster',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='roster',
            name='game',
        ),
    ]

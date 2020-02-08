# Generated by Django 3.0.2 on 2020-02-08 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20200208_0524'),
        ('roster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roster',
            name='player',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='player.Player', verbose_name='Player'),
        ),
    ]

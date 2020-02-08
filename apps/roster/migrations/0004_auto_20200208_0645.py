# Generated by Django 3.0.2 on 2020-02-08 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roster', '0003_auto_20200208_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='killteam',
            name='roster',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='killTeam', to='roster.Roster', verbose_name='Roster'),
        ),
        migrations.AlterField(
            model_name='killteammodel',
            name='killteam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='killTeamModels', to='roster.KillTeam', verbose_name='Kill Team Model'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='roster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='roster.Roster', verbose_name='Roster'),
        ),
    ]

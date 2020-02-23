# Generated by Django 3.0.2 on 2020-02-23 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_auto_20200209_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='reconnaissance_subterfuge_mission',
            field=models.CharField(blank=True, choices=[('sabatoge', 'Sabatoge Fortifications'), ('rescue', 'Rescue Prisoners'), ('seize', 'Seize Ground'), ('disrupt', 'Disrupt Supplies'), ('ambush', 'Ambush'), ('feint', 'Feint'), ('assassinate', 'Assassinate'), ('take_prisoners', 'Take Prisoners'), ('root_out', 'Root Out Enemy Agents'), ('intelligence', 'Seek Intelligence'), ('terror', 'Terror Tactics')], max_length=20, null=True, verbose_name='Extra Subterfuge Mission'),
        ),
        migrations.AlterField(
            model_name='player',
            name='reconnaissance_subterfuge_target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reconnaissance_subterfuge_targeter', to='player.Player', verbose_name='Extra Subterfuge Target'),
        ),
    ]

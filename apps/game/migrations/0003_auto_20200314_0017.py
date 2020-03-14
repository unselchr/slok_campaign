# Generated by Django 3.0.2 on 2020-03-14 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_auto_20200223_0051'),
        ('map', '0006_territory_description'),
        ('game', '0002_auto_20200223_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='phase',
            field=models.CharField(choices=[('revenue', 'Revenue Phase'), ('event', 'Event Phase'), ('challenge', 'Challenge Phase'), ('subterfuge', 'Subterfuge Phase'), ('spoils', 'Spoils Phase')], default='revenue', max_length=50, verbose_name='Phase'),
        ),
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.PositiveIntegerField(default=0, verbose_name='Turn'),
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.PositiveIntegerField(editable=False, verbose_name='Turn')),
                ('irl_location', models.CharField(max_length=50, verbose_name='Real Life Location')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles', to='game.Game', verbose_name='Game')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles', to='map.Territory', verbose_name='Location')),
                ('participants', models.ManyToManyField(related_name='battles', to='player.Player', verbose_name='Participants')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_won', to='player.Player', verbose_name='Winner')),
            ],
        ),
    ]

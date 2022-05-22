# Generated by Django 3.2 on 2022-05-21 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_score_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='batting_team',
        ),
        migrations.AlterField(
            model_name='balltoballbet',
            name='ball_num',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='overtooverbet',
            name='over_num',
            field=models.FloatField(),
        ),
    ]
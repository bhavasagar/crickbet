# Generated by Django 3.2 on 2022-05-15 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='overtooverbet',
            old_name='over_number',
            new_name='over_num',
        ),
    ]
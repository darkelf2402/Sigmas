# Generated by Django 4.0.4 on 2022-06-04 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_room_options_room_patricipants_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='patricipants',
            new_name='participants',
        ),
    ]

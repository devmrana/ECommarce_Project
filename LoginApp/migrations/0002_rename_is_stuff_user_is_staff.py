# Generated by Django 4.0.3 on 2022-11-19 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_stuff',
            new_name='is_staff',
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-16 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='address',
            new_name='address1',
        ),
        migrations.RenameField(
            model_name='useraccount',
            old_name='apartment',
            new_name='address2',
        ),
    ]
# Generated by Django 5.0.2 on 2024-03-11 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variationspecification_is_featured'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variationcategory',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='variationoption',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='variationspecification',
            old_name='name',
            new_name='title',
        ),
    ]

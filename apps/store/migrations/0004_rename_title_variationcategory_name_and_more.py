# Generated by Django 5.0.2 on 2024-03-11 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_name_variationcategory_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variationcategory',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='variationoption',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='variationspecification',
            old_name='title',
            new_name='name',
        ),
    ]

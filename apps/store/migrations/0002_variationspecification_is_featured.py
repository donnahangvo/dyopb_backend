# Generated by Django 5.0.2 on 2024-03-09 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variationspecification',
            name='is_featured',
            field=models.BooleanField(default=True),
        ),
    ]

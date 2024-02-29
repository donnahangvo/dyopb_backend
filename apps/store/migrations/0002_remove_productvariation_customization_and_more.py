# Generated by Django 5.0.2 on 2024-02-29 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariation',
            name='customization',
        ),
        migrations.RemoveField(
            model_name='productvariation',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productvariation',
            name='variation_option',
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'verbose_name': 'Product Review', 'verbose_name_plural': 'Product Reviews'},
        ),
        migrations.AlterModelOptions(
            name='variationcategory',
            options={'verbose_name': 'Variation', 'verbose_name_plural': 'Variations'},
        ),
        migrations.AlterModelOptions(
            name='variationoption',
            options={'verbose_name': 'Option', 'verbose_name_plural': 'Options'},
        ),
        migrations.AlterModelOptions(
            name='variationspecification',
            options={'verbose_name': 'Specification', 'verbose_name_plural': 'Specifications'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='variationcategory',
            name='parent',
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='variationcategory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='variationcategory',
            name='slug',
            field=models.SlugField(help_text='Category safe URL', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='variationcategory',
            name='title',
            field=models.CharField(help_text='Variation Categories - Required if there are options', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='variationoption',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='variationoption',
            name='slug',
            field=models.SlugField(help_text='Category safe URL', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='variationoption',
            name='title',
            field=models.CharField(help_text='Variation Option - not required', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='variationspecification',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='variationspecification',
            name='slug',
            field=models.SlugField(help_text='Category safe URL', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='variationspecification',
            name='title',
            field=models.CharField(help_text='Variation Specifications - not required', max_length=255, unique=True),
        ),
        migrations.DeleteModel(
            name='Customization',
        ),
        migrations.DeleteModel(
            name='ProductVariation',
        ),
    ]

# Generated by Django 5.0.2 on 2024-02-28 22:13

import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required and unique', max_length=255, unique=True)),
                ('slug', models.SlugField(help_text='Category safe URL', max_length=255, unique=True)),
                ('category_sku', models.CharField(blank=True, help_text='Defaults to slug if left blank', max_length=255, null=True, verbose_name='Category SKU')),
                ('ordering', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ('ordering',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_text', models.CharField(blank=True, help_text='Add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('title', models.CharField(help_text='Featured product name', max_length=255, unique=True)),
                ('slug', models.SlugField(help_text='Category safe URL', max_length=255, unique=True)),
                ('product_sku', models.CharField(blank=True, help_text='Defaults to slug if left blank', max_length=255, null=True, verbose_name='Product SKU')),
                ('description', models.TextField(blank=True, help_text='Not Required', max_length=10000, null=True, unique=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 9999999.99'}}, help_text='Maximum 9999999.99', max_digits=9, verbose_name='Base Price')),
                ('promotional_price', models.DecimalField(blank=True, decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 9999999.99'}}, help_text='Maximum 9999999.99', max_digits=9, null=True, verbose_name='Promotional Price')),
                ('is_featured', models.BooleanField(default=False)),
                ('num_available', models.IntegerField(default=1)),
                ('num_visits', models.IntegerField(default=0)),
                ('last_visit', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated on')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.category')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='store.product')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Full size product image', max_length=255, verbose_name='Product Image')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category safe URL')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.customization')),
                ('custom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customizations', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('stars', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VariationCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required if there are options', max_length=255, unique=True, verbose_name='Variation Category')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category safe URL')),
                ('variation_sku', models.CharField(blank=True, help_text='Defaults to slug if left blank', max_length=255, null=True, verbose_name='Variation SKU')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='store.variationcategory')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='store.product')),
            ],
            options={
                'verbose_name': 'Product Variations',
                'verbose_name_plural': 'Variation options available for product',
            },
        ),
        migrations.CreateModel(
            name='VariationOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_text', models.CharField(blank=True, help_text='Add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('title', models.CharField(help_text='Not required', max_length=255, unique=True, verbose_name='Variation Option')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category safe URL')),
                ('option_sku', models.CharField(blank=True, help_text='Defaults to slug if left blank', max_length=255, null=True, verbose_name='Option SKU')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='store.variationcategory')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.variationoption')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, help_text='Upload product image', null=True, upload_to='product_images/', verbose_name='Image')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('alt_text', models.CharField(blank=True, help_text='Add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('price_modifier', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('customization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.customization')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('variation_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variationoption')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VariationSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alt_text', models.CharField(blank=True, help_text='Add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('title', models.CharField(help_text='Not required', max_length=255, unique=True, verbose_name='Variation Option Specifications')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Category safe URL')),
                ('specification_sku', models.CharField(blank=True, help_text='Defaults to slug if left blank', max_length=255, null=True, verbose_name='Specification SKU')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='store.variationspecification')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='store.variationoption')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

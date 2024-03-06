from django.db import models

from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User

from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

# Product Image Model for Image and Thumbnail

class ProductImage(models.Model):
    image = models.ImageField(verbose_name=_('Image'), help_text=_('Upload product image'), upload_to='product_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    alt_text = models.CharField(verbose_name=_('Alternative text'), help_text=_('Add alternative text'), max_length=255, blank=True, null=True)
    # is_feature = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail_url(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                return self.save()                
            else:
                return ''

    def make_thumbnail(self, size=(300, 200)):
        img = Image.open(self.image)
        img.convert('RGB')
        thumbnail_size = (300, 200)
        img.thumbnail(thumbnail_size)

        thumb_io = BytesIO()
        img_format = self.image.name.split('.')[-1].upper()  # Extract file extension
        img.save(thumb_io, img_format, quality=85)

        thumbnail = File(thumb_io, name=self.image.name)

        return thumbnail
    
    def delete(self, *args, **kwargs):
        # Delete image files before deleting the instance
        storage, path = self.image.storage, self.image.path
        storage.delete(path)
        if self.thumbnail:
            thumb_storage, thumb_path = self.thumbnail.storage, self.thumbnail.path
            thumb_storage.delete(thumb_path)
        super().delete(*args, **kwargs)

@receiver(pre_delete, sender=ProductImage)
def product_image_delete(sender, instance, **kwargs):
    # Before deleting the instance, delete the associated image files
    instance.image.delete(False)
    if instance.thumbnail:
        instance.thumbnail.delete(False)

# Category Model
class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(help_text =_('Required and unique'), max_length=255, unique=True)
    slug = models.SlugField(help_text =_('Category safe URL'), max_length=255, unique=True)
    category_sku = models.CharField(verbose_name=_("Category SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    is_featured = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('ordering',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % (self.slug)


# Product Model
class Product(ProductImage):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    # parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(help_text=_('Featured product name'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    product_sku = models.CharField(verbose_name=_("Product SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
    price = models.DecimalField(verbose_name=_('Base Price'), help_text=_('Maximum 9999999.99'), error_messages={
            'name': {
                'max_length': _('The price must be between 0 and 9999999.99'),},}, max_digits=9, decimal_places=2)
    # promotional_price = models.DecimalField(verbose_name=_('Promotional Price'), help_text=_('Maximum 9999999.99'), error_messages={
    #         'name': {
    #             'max_length': _('The price must be between 0 and 9999999.99'),},}, max_digits=9, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    # num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)   
    created = models.DateTimeField(_('Created on'), auto_now_add=True,editable=False)
    updated = models.DateTimeField(_('Updated on'), auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
    
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0

# Product Variation Models
class VariationCategory(MPTTModel):
    variation = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(help_text=_('Variation Categories - Required if there are options'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    variation_sku = models.CharField(verbose_name=_("Variation SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    level = models.PositiveIntegerField(default=0)  # Provide a default value for the level field
    lft = models.PositiveIntegerField(default=0)  # Provide a default value for the lft field
    rght = models.PositiveIntegerField(default=0)  # Provide a default value for the rght field
    tree_id = models.PositiveIntegerField(default=0)  # Add default value for tree_id

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Variation')
        verbose_name_plural = _('Variations')


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.variation.slug, self.slug)

class VariationOption(ProductImage, MPTTModel):
    option = models.ForeignKey(VariationCategory, on_delete=models.CASCADE, related_name='options')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(help_text=_('Variation Option - not required'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    option_sku = models.CharField(verbose_name=_("Option SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)   

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/{self.option.slug}/{self.slug}/'

class VariationSpecification(ProductImage, MPTTModel):
    specification = models.ForeignKey(VariationOption, on_delete=models.CASCADE, related_name='specifications')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(help_text=_('Variation Specifications - not required'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    specification_sku = models.CharField(verbose_name=_("Specification SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
    num_available = models.IntegerField(default=1)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)   

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        verbose_name = _('Specification')
        verbose_name_plural = _('Specifications')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.specification.slug, self.slug)

    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')








# class Customization(models.Model):
#     custom = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='customizations')
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     title = models.CharField(max_length=255)
#     slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)

#     def __str__(self):
#         return self.title
    
#     def get_absolute_url(self):
#         return '/%s/%s/' % (self.custom.slug, self.slug)

# class ProductVariation(ProductImage, models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variation_category = models.ForeignKey(VariationCategory, on_delete=models.CASCADE)
#     variation_option = models.ForeignKey(VariationOption, on_delete=models.CASCADE)
#     variation_specifcation = models.ForeignKey(VariationSpecification, on_delete=models.CASCADE)
#     customization = models.ForeignKey(Customization, on_delete=models.CASCADE)
#     price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     quantity = models.PositiveIntegerField(default=0)

#     class Meta:
#         verbose_name = _('Product Variation')
#         verbose_name_plural = _('Product Variations')

#     def __str__(self):
#         return f"{self.product.title} - {self.variation_category.title} - {self.variation_option.title} - {self.variation_specifcation.title} - {self.customization.title}"
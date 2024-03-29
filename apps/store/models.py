from django.db import models

from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

# Image Handler to store and create thumbnails

class ImageHandler(models.Model):
    image = models.ImageField(upload_to='product_images/',verbose_name=_('Image'), help_text=_('Upload product image'), blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/product/thumbnails/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)
    alt_text = models.CharField(verbose_name=_('Alternative text'), help_text=_('Add alternative text'), max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.thumbnail = self.make_thumbnail(self.image)

        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            current_site = Site.objects.get_current()
            return 'http://' + current_site.domain + self.image.url
        return ''

    def get_thumbnail_url(self):
        if self.image:
            current_site = Site.objects.get_current()
            return 'http://' + current_site.domain + self.thumbnail.url if self.thumbnail else self.get_image_url()
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

    def make_thumbnail(self, image):
        if not image:
            return None

        img_format = image.name.split('.')[-1].upper()  # Extract file extension

        if img_format == 'SVG':
            # No need to resize SVG images, return the original image
            return image

        img = Image.open(image)
        img.convert('RGB')
        thumbnail_size = (300, 200)
        img.thumbnail(thumbnail_size)

        thumb_io = BytesIO()

        # Map file extensions to PIL formats
        pil_formats = {
            'JPG': 'JPEG',
            'JPEG': 'JPEG',
            'PNG': 'PNG',
            'SVG': 'SVG',
            # Add more mappings if necessary
        }

        pil_format = pil_formats.get(img_format, '.PNG')  # Default to .PNG if format is not recognized

        img.save(thumb_io, pil_format, quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def delete(self, *args, **kwargs):
        # Delete image files before deleting the instance
        storage, path = self.image.storage, self.image.path
        storage.delete(path)
        if self.thumbnail:
            thumb_storage, thumb_path = self.thumbnail.storage, self.thumbnail.path
            thumb_storage.delete(thumb_path)
        super().delete(*args, **kwargs)

@receiver(pre_delete, sender=ImageHandler)
def product_image_delete(sender, instance, **kwargs):
    # Before deleting the instance, delete the associated image files
    instance.image.delete(False)
    if instance.thumbnail:
        instance.thumbnail.delete(False)





# Category Model
class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(help_text =_('Required and unique'), max_length=255, unique=True)
    slug = models.SlugField(help_text =_('Category safe URL'), max_length=255, unique=True)
    category_sku = models.CharField(verbose_name=_("Category SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    is_featured = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('ordering',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/' % (self.slug)


# Product Model    
class Product(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(help_text=_('Featured product name'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    product_sku = models.CharField(verbose_name=_("Product SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
    price = models.DecimalField(verbose_name=_('Base Price'), help_text=_('Maximum 9999999.99'), max_digits=9, decimal_places=2, blank=True, null=True,)
    is_featured = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)
    num_visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(_('Created on'), auto_now_add=True, editable=False)
    updated = models.DateTimeField(_('Updated on'), auto_now=True)
    
    
    class Meta:
        ordering = ('ordering',)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
    
    def get_rating(self):
        total = sum(int(review['stars']) for review in self.reviews.values())

        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/product/images/')
    thumbnail = models.ImageField(upload_to='uploads/product/thumbnails/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)  


# Product Variation Models
class VariationCategory(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    product = models.ManyToManyField(Product, related_name='variation')
    name = models.CharField(help_text=_('Variation Categories - Required if there are options'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    variation_sku = models.CharField(verbose_name=_("Variation SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/variation/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/variation/thumbnails/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)
    ordering = models.IntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    lft = models.PositiveIntegerField(default=0)  
    rght = models.PositiveIntegerField(default=0)  
    tree_id = models.PositiveIntegerField(default=0) 

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Variation')
        verbose_name_plural = _('Variations')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.parent:
            return '/%s/%s/' % (self.parent.slug, self.slug)
        return '/%s/' % (self.slug)


class VariationOption(ImageHandler, MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    product = models.ManyToManyField(Product, related_name='option')
    variation = models.ForeignKey(VariationCategory, on_delete=models.CASCADE, related_name='option', default=1)
    name = models.CharField(help_text=_('Variation Option - not required'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    option_sku = models.CharField(verbose_name=_("Option SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
    price = models.DecimalField(verbose_name=_('Base Price'), help_text=_('Maximum 9999999.99'), max_digits=9, decimal_places=2, blank=True, null=True,)
    image = models.ImageField(upload_to='uploads/option/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/option/thumbnails/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)
    ordering = models.IntegerField(default=0)   

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.parent:
            return '/%s/%s/%s/' % (self.variation.slug, self.parent.slug, self.slug)
        return '/%s/%s/' % (self.variation.slug, self.slug)
    

class VariationSpecification(ImageHandler, MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    product = models.ManyToManyField(Product, related_name='specification')
    option = models.ForeignKey(VariationOption, on_delete=models.CASCADE, related_name='specification', default=1)
    name = models.CharField(help_text=_('Variation Specifications - not required'), max_length=255, unique=True)
    slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
    specification_sku = models.CharField(verbose_name=_("Specification SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
    description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
    price = models.DecimalField(verbose_name=_('Base Price'), help_text=_('Maximum 9999999.99'), max_digits=9, decimal_places=2, blank=True, null=True,)
    num_available = models.IntegerField(default=None, null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/specification/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/specification/thumbnails/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True) 
    ordering = models.IntegerField(default=0)   

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        verbose_name = _('Specification')
        verbose_name_plural = _('Specifications')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        if self.parent:
            return '/%s/%s/%s/' % (self.option.variation.slug, self.option.slug, self.slug)
        return '/%s/%s/' % (self.option.slug, self.slug)
    




class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    stars = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/product_reviews/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/product_reviews/images/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)   

    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')











    # def delete(self, *args, **kwargs):
    #     # Delete image files before deleting the instance
    #     storage, path = self.image.storage, self.image.path
    #     storage.delete(path)
    #     if self.thumbnail:
    #         thumb_storage, thumb_path = self.thumbnail.storage, self.thumbnail.path
    #         thumb_storage.delete(thumb_path)
    #     super().delete(*args, **kwargs)



    # def get_absolute_url(self):
    #     return '/%s/%s/' % (self.variation.slug, self.slug)

    # def get_absolute_url(self):
    #     return f'/{self.option.slug}/{self.slug}/'


    # def get_absolute_url(self):
    #     return '/%s/%s/' % (self.specification.slug, self.slug)
    
# # Product Variation Models
# class ProductVariation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variation = models.ForeignKey(VariationCategory, on_delete=models.CASCADE)
#     option = models.ForeignKey(VariationOption, on_delete=models.CASCADE, null=True, blank=True)
#     specification = models.ForeignKey(VariationSpecification, on_delete=models.CASCADE, null=True, blank=True)

#     class Meta:
#         verbose_name = _('Product Variation')
#         verbose_name_plural = _('Product Variations')
#         unique_together = ('product', 'variation', 'option', 'specification')

#     def get_options(self):
#         return self.variation.option_set.all()

#     def get_specifications(self):
#         return self.variation.specification_set.all()



# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
#     # parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(help_text=_('Featured product name'), max_length=255, unique=True)
#     slug = models.SlugField(help_text=_('Category safe URL'), max_length=255, unique=True)
#     product_sku = models.CharField(verbose_name=_("Product SKU"), max_length=255, blank=True, null=True, help_text=_("Defaults to slug if left blank"))
#     description = models.TextField(verbose_name=_('Description'),help_text=_('Not Required'), max_length=10000, blank=True, null=True)
#     price = models.DecimalField(verbose_name=_('Base Price'), help_text=_('Maximum 9999999.99'), error_messages={
#             'name': {
#                 'max_length': _('The price must be between 0 and 9999999.99'),},}, max_digits=9, decimal_places=2)
#     is_featured = models.BooleanField(default=False)
#     num_visits = models.IntegerField(default=0)
#     last_visit = models.DateTimeField(blank=True, null=True)
#     image = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     thumbnail = models.ImageField(upload_to='uploads/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)   
#     created = models.DateTimeField(_('Created on'), auto_now_add=True,editable=False)
#     updated = models.DateTimeField(_('Updated on'), auto_now=True)
#     ordering = models.IntegerField(default=0)
#         # promotional_price = models.DecimalField(verbose_name=_('Promotional Price'), help_text=_('Maximum 9999999.99'), error_messages={
#     #         'name': {
#     #             'max_length': _('The price must be between 0 and 9999999.99'),},}, max_digits=9, decimal_places=2, blank=True, null=True)
#     # num_available = models.IntegerField(default=1)

#     class Meta:
#         ordering = ('-created',)

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return '/%s/%s/' % (self.category.slug, self.slug)
    
#     def get_rating(self):
#         total = sum(int(review['stars']) for review in self.reviews.values())

#         if self.reviews.count() > 0:
#             return total / self.reviews.count()
#         else:
#             return 0

# class ProductImage(ImageHandler, models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     thumbnail = models.ImageField(upload_to='uploads/', help_text=_('Automatically generated, do not need to upload'), blank=True, null=True)









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
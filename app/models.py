from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.conf import settings
from . mixins import ImageCleanupMixin 
from django.core.exceptions import ValidationError

mobile_validator = RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit mobile number.")

class Category(models.Model, ImageCleanupMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')
    short_description = HTMLField()
    description = HTMLField()
    faq = HTMLField()
    key_insights = HTMLField()
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_subcategories(self):
        return self.children.all()
    
    def is_leaf_node(self):
        return not self.children.exists()

    def is_root(self):
        return self.parent is None

    def save(self, *args, **kwargs):
        if self.pk:
            self.delete_old_file('image')
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_file_on_delete('image')
        super().delete(*args, **kwargs)

class Location(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='location')
    short_description = HTMLField()
    description = HTMLField()
    faq = HTMLField()
    key_insights = HTMLField()
    slug = models.SlugField(unique=True, blank=True)  # NEW


    # Here's the magic: parent can point to another Location
    parent = models.ForeignKey(
        'self',              # reference the same Location model
        on_delete=models.CASCADE,
        null=True,           # allow no parent for main Location
        blank=True,
        related_name='children'  # lets you access all sublocation easily
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_sublocations(self):
        return self.children.all()

    def is_root(self):
        return self.parent is None
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            unique_slug = base_slug
            counter = 1
            while Location.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            self.delete_old_file('image')
        if not self.slug:
            ...
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.delete_file_on_delete('image')
        super().delete(*args, **kwargs)

class Business(models.Model, ImageCleanupMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_district = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="District")
    business_type = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Business Category")
    business_name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Business name")
    business_description = models.TextField(verbose_name="Business Description")
    business_address = models.TextField(verbose_name="Business Address", default="not provided")
    business_since = models.DateField(verbose_name="Business Since", null=True, blank=True)
    business_contact = models.CharField(max_length=10, validators=[mobile_validator], null=False, blank=False, verbose_name="Business Mobile")
    business_whatsapp = models.CharField(max_length=10, validators=[mobile_validator], null=False, blank=False, verbose_name="Business Whatsapp")

    slug = models.SlugField(unique=True, blank=True)

    # Business Images
    business_image_1 = models.ImageField(upload_to='business_images/', null=False, blank=False, verbose_name="Profile Picture")
    business_image_2 = models.ImageField(upload_to='business_images/', null=True, blank=True, verbose_name="Image 1")
    business_image_3 = models.ImageField(upload_to='business_images/', null=True, blank=True, verbose_name="Image 2")
    business_image_4 = models.ImageField(upload_to='business_images/', null=True, blank=True, verbose_name="Image 3")
    business_image_5 = models.ImageField(upload_to='business_images/', null=True, blank=True, verbose_name="Image 4")
    business_logo = models.ImageField(upload_to='business_logo/', null=True, blank=True, verbose_name="business logo")

    # Social Links
    business_instagram_link = models.URLField(null=True, blank=True, verbose_name="Instagram link")
    business_facebook_link = models.URLField(null=True, blank=True, verbose_name="Facebook Link")
    business_youtube_link = models.URLField(null=True, blank=True, verbose_name="Youtube Link")
    business_x_link = models.URLField(null=True, blank=True)
    business_mail = models.CharField(max_length=100,null=True,blank=True)
    business_website = models.URLField(null=True, blank=True, verbose_name="Website Link")

    business_location = models.TextField(null=True, blank=True, verbose_name="Location")
    active = models.BooleanField(default=False)

    # Account type
    premium = models.BooleanField(default=False)
    trusted = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)


    # statistics
    views_count = models.IntegerField(default=0)
    is_top_in_category = models.BooleanField(default=False)  # manually select in admin
    top_rank = models.PositiveIntegerField(null=True, blank=True)  # optional: to set order among top 10

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.business_name
    

    def clean(self):
        if not self.category.is_leaf_node():
            raise ValidationError("Only leaf categories are allowed for businesses.")

    def save(self, *args, **kwargs):
        if self.pk:
            # Delete old images if they were replaced
            for field in [
                'business_image_1', 'business_image_2', 'business_image_3',
                'business_image_4', 'business_image_5'
            ]:
                self.delete_old_file(field)

        if not self.slug:
            base_slug = slugify(self.business_name)
            unique_slug = base_slug
            counter = 1
            while Business.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete images on delete
        for field in [
            'business_image_1', 'business_image_2', 'business_image_3',
            'business_image_4', 'business_image_5'
        ]:
            self.delete_file_on_delete(field)
        super().delete(*args, **kwargs)

class Enquiry(models.Model):
    enquired_business = models.ForeignKey(Business,on_delete=models.CASCADE)
    message = models.TextField()
    enquired_person = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.enquired_person.username} → {self.enquired_business.business_name}'
    
class Leads(models.Model):
    visited_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    visited_business = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating must be between 1 and 5"
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviewer.username} rated {self.business.business_name} {self.rating} stars'

    class Meta:
        unique_together = ('reviewer', 'business')  # One review per user per business
        ordering = ['-created_at']








    












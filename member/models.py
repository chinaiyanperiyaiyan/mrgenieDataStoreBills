from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# ============================================================
# SHOP MODEL
# ============================================================
class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shops")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    # Branding
    logo = models.ImageField(upload_to='shop_logos/' , blank=True , null= True )
    banner_image = models.ImageField(upload_to='shop_banners/', blank=True, null=True)
    banner_title = models.CharField(max_length=255, default="Welcome to our shop!")
    banner_text = models.TextField(blank=True, null=True)

    # About Section
    about_title = models.CharField(max_length=255, blank=True, null=True)
    about_description = models.TextField(blank=True, null=True)
    about_details = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    # Contact Info
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)
    contact_hours = models.CharField(max_length=100, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# PRODUCT MODEL
# ============================================================
class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon_class = models.CharField(max_length=100, default="fas fa-box")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.shop.name}"


# ============================================================
# BILL MODEL
# ============================================================
class Bill(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='bills')
    bill_no = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_mobile = models.CharField(max_length=20, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    bill_image = models.ImageField(upload_to='bills/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    download_expiry = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-set expiry 1 hour after creation if not manually set
        if not self.download_expiry:
            self.download_expiry = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_downloadable(self):
        return timezone.now() <= self.download_expiry

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.bill_no} - {self.shop.name}"


# ============================================================
# OFFER MODEL
# ============================================================
class Offer(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ["-start_time"]

    def __str__(self):
        return f"{self.title} - {self.shop.name}"


# ============================================================
# VIDEO MODEL
# ============================================================
class Video(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.shop.name}"


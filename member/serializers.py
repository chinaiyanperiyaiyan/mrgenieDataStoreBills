from rest_framework import serializers
from .models import Shop, Product

# ----------------------
# Product Serializer
# ----------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'icon_class', 'price', 'description']

# ----------------------
# Offer Serializer
# ----------------------
# class OfferSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Offer
#         fields = ['title', 'description', 'image', 'start_time', 'end_time']

# ----------------------
# Video Serializer
# ----------------------
# class VideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Video
#         fields = ['title', 'video_url']

# ----------------------
# Shop Serializer (nested)
# ----------------------
class ShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    # offers = OfferSerializer(many=True, read_only=True)
    # videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = [
            'id',
            'name',
            'logo',
            'banner_title',
            'banner_text',
            'about_title',
            'about_description',
            'about_details',
            'contact_phone',
            'contact_email',
            'contact_address',
            'contact_hours',
            'whatsapp_number',
            'products',
            # 'offers',
            # 'videos',
        ]

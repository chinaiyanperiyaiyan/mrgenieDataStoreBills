# from django.shortcuts import render
from django.http import HttpResponse
# member/views.py
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bill, Shop
# from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.conf import settings

@csrf_exempt
def upload_bill_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            storeName = data.get('storeName')
            bill_no = f"{data.get('bill_no')+storeName}".replace(" " , "")
            customer_name = data.get('customer_name')
            customer_mobile = data.get('customer_mobile')
            customer_email = data.get('customer_email')
            image_data = data.get('image')  # Base64 image string

            if not all([storeName, bill_no, image_data]):
                return JsonResponse({"status": "fail", "error": "Missing required fields"})

            # Get the shop
            try:
                shop = Shop.objects.get(name=storeName)
            except Shop.DoesNotExist:
                return JsonResponse({"status": "fail", "error": f"Shop '{storeName}' not found"})

            # Process the image
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"{bill_no}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            # Save the bill
            bill = Bill.objects.create(
                shop=shop,
                bill_no= bill_no,
                customer_name=customer_name,
                customer_mobile=customer_mobile,
                customer_email=customer_email,
                bill_image=image_file
            )

            return JsonResponse({"status": "success", "bill_id": bill.id})

        except Exception as e:
            # Return the actual error message for debugging
            return JsonResponse({"status": "error", "error": str(e)})

    return JsonResponse({"status": "fail", "error": "Invalid request method"})

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import ShopSerializer

# ----------------------
# Shop List API
# ----------------------
# class ShopListAPI(APIView):
#     def get(self, request):
#         shops = Shop.objects.all()
#         serializer = ShopSerializer(shops, many=True)
#         # return Response(serializer.data)
#         return JsonResponse({"status": "success"})

# ----------------------
# Shop Detail API
# ----------------------
# class ShopDetailAPI(APIView):
#     def get(self, request, pk):
#         shop = Shop.objects.prefetch_related('products', 'offers', 'videos').get(pk=pk)
#         serializer = ShopSerializer(shop)
#         return Response(serializer.data)
from django.shortcuts import get_object_or_404

def ShopDetailAPI(request, id):
    # Get single shop or 404
    shop = get_object_or_404(
        Shop.objects.prefetch_related('products', 'offers', 'videos'),
        pk=id
    )

    # Build a single dictionary for this shop
    shop_data = {
        "id": shop.id,
        "name": shop.name,
        "slug": shop.slug,
        "description": shop.description,
        "logo": request.build_absolute_uri(shop.logo.url) if shop.logo else None,
        "banner_image": request.build_absolute_uri(shop.banner_image.url) if shop.banner_image else None,
        "banner_title": shop.banner_title,
        "banner_text": shop.banner_text,
        "about_title": shop.about_title,
        "about_description": shop.about_description,
        "about_details": shop.about_details,
        "video_url": shop.video_url,
        "contact": {
            "phone": shop.contact_phone,
            "email": shop.contact_email,
            "address": shop.contact_address,
            "hours": shop.contact_hours,
            "whatsapp": shop.whatsapp_number
        },
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": str(p.price),
                "icon_class": p.icon_class,
            } for p in shop.products.all()
        ],
        "offers": [
            {
                "id": o.id,
                "title": o.title,
                "description": o.description,
                "image": request.build_absolute_uri(o.image.url) if o.image else None,
                "start_time": o.start_time,
                "end_time": o.end_time,
            } for o in shop.offers.all()
        ],
        "videos": [
            {
                "id": v.id,
                "title": v.title,
                "video_url": v.video_url,
            } for v in shop.videos.all()
        ],
    }

    return JsonResponse({"shop": shop_data}, safe=False)


def ShopListAPI (request):
    shops = Shop.objects.all()
    shops_list = []
    for shop in shops:
        shop_data = {
            "shop_id":shop.id ,
            "shop_name": shop.name,
            "slug": shop.slug,
            "description": shop.description,
            "logo": request.build_absolute_uri(shop.logo.url) if shop.logo else None,
            }
        shops_list.append(shop_data)
    return JsonResponse({"status": "success" , "shops_list":shops_list})

import os
from datetime import datetime

def download_bill_image(request):
    try:
        prefix = "TRP"
        date_str = datetime.now().strftime("%m%d%Y")
        shop_id = request.GET.get("shopId")
        shop_name = request.GET.get("shopName")
        otp = request.GET.get("otp")  # optional if needed for validation
        bill_no_get = request.GET.get("billNo")

        bill_no = prefix+date_str+bill_no_get

        if not all([shop_id , shop_name, bill_no , otp ]):
            return JsonResponse({"status": "error", "message": "Missing required parameters" }, status=400)

        shop = get_object_or_404(Shop, id=shop_id, name=shop_name)
        bill_no_included = f"{bill_no+shop_name}".replace(" " , "")

        bill = Bill.objects.filter(shop=shop, bill_no=bill_no_included , customer_mobile=otp).first()

        if not bill:
            return JsonResponse({"status": "error", "message": "Bill not found"}, status=404)

        if not bill.bill_image:
            return JsonResponse({"status": "error", "message": "Bill image not available"}, status=404)

        bill_url = request.build_absolute_uri(bill.bill_image.url)
        image_path = os.path.join(settings.MEDIA_ROOT, bill.bill_image.name)

        if not os.path.exists(image_path):
            return JsonResponse({"status": "error", "message": "Bill image file missing on server"}, status=404)

        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

        return JsonResponse({
            "status": "success",
            "bill_image_base64": encoded_string,
            "bill_no":bill_no,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "success"})


def Home(request):
    return HttpResponse("""<h1 style = "background-color:red;">Welcome to Home page
                        <a href = '/admin/'>Admin</a></h1>""")
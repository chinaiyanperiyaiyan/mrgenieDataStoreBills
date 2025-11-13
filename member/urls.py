
from django.urls import path , include
from . import views

urlpatterns = [
    path('' , views.Home , name="home" ),
    path('home/' , views.Home , name="home" ),
    path('upload_bill_image/', views.upload_bill_image, name='upload_bill_image'),
    path('download_bill_image/', views.download_bill_image , name='download_bill_image'),
    path('api/shops/', views.ShopListAPI, name='shop-list-api'),
    path('api/shop/<int:id>/', views.ShopDetailAPI, name='shop-detail-api'),
]

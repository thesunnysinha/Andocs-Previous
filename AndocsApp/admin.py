from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    Profile,
    Wishlist,
    Comment,
    Cluster,
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=[
        'id','user','name','locality','city','zipcode','state','mobile_number'
    ]

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
            'id','title','selling_price','discounted_price','description','brand','country','category','sub_category','product_image'
    ]

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = [
            'id', 'user','product','quantity','date_added'
    ]

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = [
            'id', 'user','customer','product','quantity','status','transaction_id','date_ordered',
    ]

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = [
            'user','phone_num','gender','birth_date','profile_pic',
    ]


@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = [
            'id', 'user','product','quantity','date_added'
    ]

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = [
            'user_name','product','id','rating','comment','create_at','update_at','ip',
    ]
    list_filter = ['create_at', 'user_name']
    search_fields = ['comment']

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']
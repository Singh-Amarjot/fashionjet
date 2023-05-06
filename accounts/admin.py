from django.contrib import admin
from .models import *
admin.site.register(CartItems)

class CartAdmin(admin.ModelAdmin):
    list_display=['uid','user','is_paid','razor_pay_order_id','razor_pay_payment_id']
admin.site.register(Cart,CartAdmin)
admin.site.register(Profile)

# Register your models here.

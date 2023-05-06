from django.shortcuts import render,redirect
from .models import Product,SizeVariant 

# from django.http import HttpResponseRedirect
# from accounts.models import Cart,CartItems
# Create your views here.


def get_product(request , slug):
    # print("***************************")
    # print(request.user)
    # print('***************************')
    # print(request.user.profile.get_cart_count)
    
    try:
        product = Product.objects.get(slug =slug)
        context={'product':product}

        if request.GET.get("size"):
            size=request.GET.get('size')
            # print(size)
            price=product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            # print(price)

        return render(request  , 'product/product.html' , context = context)

    except Exception as e:
        return redirect('login')
        print(e)
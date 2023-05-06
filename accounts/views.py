from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
import razorpay

def signout(request):
    logout(request)
    return redirect('index')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        
        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)

    return render(request ,'accounts/register.html')

def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    
def add_to_cart(request,uid):
    try:
        variant=request.GET.get('select_size')
        quantity=request.GET.get('qcounter')
        print(quantity)
        product=Product.objects.get(uid=uid)
        user=request.user
        cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    
        cart_items = CartItems.objects.create(cart=cart,product=product)
    
        if variant:
            variant=request.GET.get('select_size')
            print("Working ",variant)
            size_variant=SizeVariant.objects.get(size_name=variant)
            print(size_variant)
            cart_items.size_variant=size_variant
            cart_items.save()
        print('Done')
    
        if quantity:
            quantity=request.GET.get('qcounter')
            print("Quantity",quantity)
            cart_items.quantity=quantity
            cart_items.save()
    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return redirect('login')
        print(e)
    


def remove_cart(request,cart_item_uid):
    try:
        cart_item=CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
from django.conf import settings
def cart(request):
    try:
        cart_obj= CartItems.objects.filter(cart__is_paid=False,cart__user=request.user) #use for fetch Cartitems function
        cart_total= Cart.objects.filter(is_paid=False,user=request.user).first() #for count only cart items 
    except Exception as e:
        return redirect('login')
        print(e)
    print("Coupon --------------------------------",Coupon.objects.all())
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code =coupon.upper()).first()
        if not coupon_obj:
            messages.warning(request,'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        cart_coupon=Cart.objects.filter(coupon=coupon_obj, user= request.user, is_paid=False).first()
        if cart_coupon:
            messages.success(request,'Coupon Already Applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # new code for discount show
        if cart_total.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request,f'Amount should be Greater than {coupon_obj.minimum_amount}.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if  coupon_obj.is_expired:
            messages.warning(request,f'Coupon Expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            cartuser= Cart.objects.get(user=request.user,is_paid=False)
            cartuser.coupon=coupon_obj
            cartuser.save()
            messages.success(request,'Coupon Applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # payment gateway code --------------------------------
    if cart_obj:
        client=razorpay.Client(auth=(settings.KEY, settings.SECRET) )
        payment=client.order.create({'amount':cart_total.get_cart_total()*100,'currency':'INR','payment_capture':1})
        print("******************************************************\n",payment,"\n***************************************")
        cart_total.razor_pay_order_id=payment['id']
        cart_total.save()
        # payment gateway code --------------------------------
        context={"cart":cart_obj, 'total': cart_total,'payment':payment}
        return render(request,'accounts/cart.html',context)
    context={"cart":cart_obj, 'total': cart_total}
    return render(request,'accounts/cart.html',context)

def remove_coupon(request,cart_uid):
            cart=Cart.objects.get(uid=cart_uid)
            print("cart uid ---------------------------------------------------------",cart)
            print("Coupon Check Before ----------------------------------------------",cart.coupon)
            cart.coupon=None
            print("Coupon Check After ----------------------------------------------",cart.coupon)
            cart.save()
            messages.success(request,'Coupon Removed')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
    try:
        order_id=request.GET.get('razorpay_order_id')
        payment_id=request.GET.get('razorpay_payment_id')
        signature=request.GET.get('razorpay_signature')
        
        
        cart=Cart.objects.get(razor_pay_order_id = order_id)
        cart.razor_pay_payment_id=payment_id
        cart.razor_pay_payment_signature=signature
        cart.is_paid=True
        cart.save()
        user = cart.user
        context = {
            'razorpay_id': order_id,
            'user_name': user.username,
            "cart":cart
        }
        return render(request, 'success/success.html', context)
        # return HttpResponse('Payment Success')
    except Exception as e:
        print(e)
        return HttpResponse('Payment Not Success')

def invoice(request):
    return render(request,'invoice/invoice.html') 
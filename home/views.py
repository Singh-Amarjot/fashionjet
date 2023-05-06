from django.shortcuts import render,redirect
from products.models import Product, Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import contact


def index(request):
    context = {'products' : Product.objects.all(),'categories':Category.objects.all()}
    if request.method=="POST":
       search= request.POST.get('search_item')
       print(search)
       try:
        searched_item=Product.objects.filter(product_name__icontains=search)
        print("check",searched_item)
        # context['searched_item']=searched_item
        context={'products':searched_item}
        print("hii",context)
        return render(request , 'home/index.html' , context)
       except Exception as e:
        print(e)
    return render(request , 'home/index.html' , context)
def contactform(request):
    if request.method == 'POST':
        name=request.POST['name']
        print("********************************************",name)
        email=request.POST['email']
        subject=request.POST['subject']
        desc=request.POST['desc']
        contact.objects.create(name=name,email=email,subject=subject,desc=desc)
        messages.success(request,"Your message was sent, thank you!")
        # return HttpResponseRedirect(request.path_info)
        return redirect(request.path_info)
    return render(request,'accounts/contact.html') 

def category_show(request,cname):
    products=Product.objects.filter(category__category_name=cname)
    context = {'products' : products}

    return render (request , 'home/categories.html' , context)




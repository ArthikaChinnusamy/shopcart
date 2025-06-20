from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.shortcuts import redirect

# from django.http import HttpResponse
from shop.form import CustomUserForm

from django.contrib.auth import authenticate,login,logout

from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'shop/index.html',context={'products':products}
) 
def loginpage(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method=='POST':
            name=request.POST['username']
            pwd=request.POST['password']
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect(home)
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect('login')
    return render(request,'shop/login.html')

def loginoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged out Successfully')
    return redirect(home)

def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration success, You can Login Now..!")
            return redirect('login')  #/login........
    return render(request,'shop/register.html', context={'form':form}
) 
def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',context={'catagory':catagory}) 

def collectionsview(request,name):    
    if (Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,'shop/products/index.html',context={'products':products,'catagory':name} )
    else:
        messages.warning(request,'no such product found')
        return redirect('collections')

def productdetails(request,cname,pname):    
    if (Catagory.objects.filter(name=cname,status=0)):
        if (Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first() #..........first()
            return render(request,'shop/products/productdetails.html',context={'products':products,'catagory':cname} )
        else:   
            messages.warning(request,'no such product found')
            return redirect('collections')
    else:
        messages.warning(request,'no such product found')
        return redirect('collections')
    # return HttpResponse("product")

def addtocart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added in Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not Available'},status=200)
                    
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    
def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'shop/cart.html',context={'cart':cart})
    else:
        return redirect('home')
    
def removecart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')


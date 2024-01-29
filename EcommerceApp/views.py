from django.shortcuts import render

from django.shortcuts import render,redirect
from django.conf.urls.static import static
from django.db import IntegrityError
from EcommerceApp.models import Category
from EcommerceApp.models import Product
from EcommerceApp.models import Customer
from EcommerceApp.models import Cart
from django.conf import settings
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.db.models import F
from django.contrib.auth.decorators import login_required

import os

def home(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None

        return render(request, 'home.html', {'cat': cat, 'cust': cust})
    else:
        return render(request, 'home.html')


def login(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        return render(request,'loginpage.html',{'cat':cat})
    else:
        return render(request,'loginpage.html')

def signup(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        return render(request,'signuppage.html',{'cat': cat})
    else:
        return render(request,'signuppage.html')

def review(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None
        return render(request,'review.html',{'cat': cat,'cust': cust})
    else:
        return render(request,'review.html')    
    

def aboutus(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None
        return render(request,'aboutus.html',{'cat': cat,'cust': cust})
    else:
        return render(request,'aboutus.html')      

def navbarhome(request):
    if request.user.is_authenticated:
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None
        return render(request, 'navbarhome.html', {'cust': cust})
    else:
        return render(request, 'navbarhome.html')

def navbarcustomer(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        return render(request, 'customer/navbarcustomer.html', {'cat': cat})


def main_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr = auth.authenticate(username=username,password=password)
        if usr is not None:
            if usr.is_staff:
                auth.login(request,usr)
                return render(request,'admin/admin_page.html')
            else:
                auth.login(request,usr)
                cat = Category.objects.all()
                try:
                    cust = Customer.objects.get(customer_name=request.user)
                except Customer.DoesNotExist:
                    cust = None
                return render(request,'customer/customer_home.html',{'cat':cat,'cust':cust})
        else:
            messages.error(request,'Invalid Username or Password')
            return redirect('login')
        
def admin_page(request):
    return render(request,'admin/admin_page.html') 

def add_category(request):
    return render(request,'admin/admin_category.html')

def register_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cat_name = request.POST.get('cat_name')
            cat = Category(category_name=cat_name)
            cat.save()
            messages.success(request,'Category Added Successfully')
            return redirect('add_category')
        
def add_product(request):
    cat = Category.objects.all()
    return render(request,'admin/admin_product.html',{'cat':cat})

def register_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cat_name = request.POST.get('sel')
            pro_name = request.POST.get('pdt_name')
            pro_price = request.POST.get('pdt_price')
            pro_description = request.POST.get('pdt_desc')
            pro_image = request.FILES.get('pdt_image')
            cat = Category.objects.get(id=cat_name)
            pro = Product(categoryf_name=cat,product_name=pro_name,product_price=pro_price,product_description=pro_description,product_image=pro_image)
            pro.save()
            messages.success(request,'Product Added Successfully')
            return redirect('view_product')
        
def view_product(request):
    pro = Product.objects.all()
    return render(request,'admin/admin_viewproduct.html',{'pro':pro})

def product_delete(request,pk):
    if request.user.is_authenticated:
        pro = Product.objects.get(id=pk)
        pro.delete()
        messages.success(request,'Product Deleted Successfully')
        return redirect('view_product')
        
def admin_logout(request):
    auth.logout(request)
    return redirect('home')

def register_customer(request):
        if request.method == 'POST':
            firstname  = request.POST.get('fname')
            lastname = request.POST.get('lname')
            usrname = request.POST.get('uname')
            mail = request.POST.get('email')
            password = request.POST.get('pass')
            cpassword = request.POST.get('cpass')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            image = request.FILES.get('image')
            if password == cpassword:
                if User.objects.filter(username=usrname).exists():
                    messages.error(request,'Username Already Exists')
                    return redirect('signup')
                else:
                    usr = User.objects.create_user(username=usrname, email=mail, password=password,first_name=firstname,last_name=lastname)
                    cust = Customer(customer_name=usr,customer_address=address,customer_number=contact,customer_image=image)
                    usr.save()
                    cust.save()
                    messages.success(request,'Customer Added Successfully')
                    return redirect('signup')
            else:
                messages.error(request,'Password Does Not Match')
                return redirect('signup')
            
def view_users(request):
    cust = Customer.objects.all()
    return render(request,'admin/customer_details.html',{'cust':cust})

def customer_delete(request,pk):
    if request.user.is_authenticated:
        cust = Customer.objects.get(id=pk)
        usr = User.objects.get(username = cust.customer_name.username)
        cust.delete()
        usr.delete()
        messages.success(request,'Customer Deleted Successfully')
        return redirect('view_users')


def footer_customer(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()
        return render(request,'customer/footer_customer.html',{'cat':cat})
    else:
        return render(request,'customer/footer_customer.html')    

   
def customer_products(request, pk):
    if request.user.is_authenticated:
        catss = Category.objects.all()
        
        cat = Category.objects.get(id=pk)
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None
        pdt = Product.objects.filter(categoryf_name=cat)
        return render(request, 'customer/customer_products.html', {'pdt': pdt, 'cat': catss, 'selected_category': pk,'cust': cust})
    

def all_products(request):
    if request.user.is_authenticated:   
        catss = Category.objects.all()
        cust = Customer.objects.get(customer_name=request.user)
        pdt = Product.objects.all()
        return render(request, 'customer/all_products.html', {'pdt': pdt, 'cat': catss, 'cust': cust})
    else:
        return redirect('/')



@login_required
def add_to_cart(request, pk):
    pro = Product.objects.get(id=pk)
    cart_item, created = Cart.objects.get_or_create(user_cart=request.user,user_product=pro)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    
    catss = Category.objects.all()
    messages.success(request, 'Product Added To Cart')
    return redirect('cart_view')
    
    

def cart_remove(request, pk):   
    if request.user.is_authenticated:
        pro = Product.objects.get(id=pk)
        cart_item = Cart.objects.filter(user_cart=request.user, user_product=pro)
        if cart_item:
            cart_item.delete()
        return redirect('cart_view')    


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user_cart=request.user).select_related('user_product')
        total_price = sum(item.total_price() for item in cart_items)
        cat = Category.objects.all()
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None
        return render(request, 'customer/cart.html', {'cart': cart_items, 'total_price': total_price,'cust':cust,'cat':cat})

def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user_cart=request.user).select_related('user_product')
        total_price = sum(item.total_price() for item in cart_items)
        crt = Cart.objects.filter(user_cart=request.user)
        catss = Category.objects.all()
        try:
            cust = Customer.objects.get(customer_name=request.user)
        except Customer.DoesNotExist:
            cust = None
        return render(request, 'customer/checkoutdetails.html', {'cart': cart_items, 'total_price': total_price,'cart':crt,'cust':cust,'catss':catss})

def customer_logout(request):
    auth.logout(request)
    return redirect('home') 

def decrement(request,pk):
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(user_product_id =pk, user_cart=request.user)
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('cart_view')

def increment(request,pk):  
    if request.user.is_authenticated:
        cart_item = Cart.objects.get(user_product_id =pk, user_cart=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart_view')     

def checkout_process(request):
    return render(request,'customer/checkoutsuccess.html')

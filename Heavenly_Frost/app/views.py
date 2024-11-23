from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def shop_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
    
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['shop']=uname      # create
                    return redirect(shop_home)
                else:
                    req.session['user']=uname      # create
                    return redirect(user_home)
            else:
                messages.warning(req,"invalid uname or password")  
        return render(req,'login.html') 

def shop_logout(req):
    logout(req)
    req.session.flush()             # delete 
    return redirect(shop_login) 

def  register(req):
     if req.method=='POST':
        name=req.POST['name']       
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=User.objects.create_user(first_name=name,username=email,email=email,password=password)
            data.save()
            return redirect(shop_login)
        except:
            messages.warning(req,"user details already exits")
            return redirect(register)
     else:
         return render(req,'register.html')
          

#--------------------- admin-------------------------------------------------------------------------------------------  

def shop_home(req):
    if 'shop' in req.session:
        products=Cake.objects.all()
        return render(req,'shop/shop_home.html',{'Cake':products})
    else:
        return redirect(shop_login)  


def add_product(req):
    if req.method=='POST':
        id=req.POST['cake_id']
        name=req.POST['cake_name']       
        price=req.POST['price']            
        file=req.FILES['img']
        cat=req.POST['category']
        colour=req.POST['colour']
        qty=req.POST['quantity']
        des=req.POST['description']
        data=Cake.objects.create(cake_id=id,cake_name=name,price=price,img=file,category=cat,colour=colour,quantity=qty,description=des)   
        data.save()
        return redirect(shop_home)
    return render(req,'shop/add_pro.html') 


def edit_pro(req,id):
        cake=Cake.objects.get(pk=id)
        if req.method=='POST':
            id=req.POST['cake_id']
            name=req.POST['cake_name']       
            price=req.POST['price'] 
            file=req.FILES['img']      
            cat=req.POST['category']
            clr=req.POST['colour']    
            qty=req.POST['quantity']
            des=req.POST['description']   
            
            print(file)
            if file:
                Cake.objects.filter(pk=id).update(cake_id=id,cake_name=name,price=price,img=file,category=cat,colour=clr,quantity=qty,description=des)   
            else:
                Cake.objects.filter(pk=id).update(cake_id=id,cake_name=name,price=price,category=cat,colour=clr,quantity=qty,description=des)   

            return redirect(shop_home)
        return render(req,'shop/edit_pro.html',{'data':cake}) 


def delete_pro(req,id):
        data=Cake.objects.get(pk=id)
        url=data.img.url
        url=url.split('/')[-1]
        os.remove('media/'+url)  
        data.delete()
        return redirect(shop_home) 


def bookings(req):
    bookings=Buy.objects.all()[::-1][:10]
    return render(req,'shop/bookings.html',{'data':bookings})


# #------------------------------------- User--------------------------------------------------------------

def user_home(req):
    if 'user' in req.session:
        products=Cake.objects.all()
        return render(req,'user/user_home.html',{'product':products})                  


def view_pro(req,id):
     log_user=User.objects.get(username=req.session['user'])
     products=Cake.objects.get(pk=id)
     try:
         cart=Cart.objects.get(product=products,user=log_user)
     except:
         cart=None    
     return render(req,'user/view_pro.html',{'product':products,'cart':cart}) 


def add_to_cart(req,id):
     products=Cake.objects.get(pk=id)
     print(products)
     user=User.objects.get(username=req.session['user'])
     print(user)
     data=Cart.objects.create(user=user,cake=products)
     data.save()
     return redirect(cart_display)


def cart_display(req):
    log_user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=log_user)
    return render(req,'user/cart_display.html',{'data':data})  


def delete_cart(req,id):
    data=Cart.objects.get(pk=id) 
    data.delete()
    return redirect(cart_display)


def buy_pro(req,id):
    products=Cake.objects.get(pk=id)
    user=User.objects.get(username=req.session['user'])
    price=products.price
    data=Buy.objects.create(user=user,cake=products,price=price)
    # data = Buy.objects.create(user=user, cake=products)
    data.save()
    return redirect(user_home)


def user_view_bookings(req):
    user=User.objects.get(username=req.session['user'])
    data=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/view_bookings.html',{'data':data})
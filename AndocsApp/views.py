from django.shortcuts import render,redirect
from django.views import View,generic
from .models import Customer,Product,Cart,OrderPlaced,UserOtp,Wishlist,Comment,Cluster
from .forms import SignUpForm,CustomerProfileForm,UserUpdateForm,UserProfileUpdateForm,CommentForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from .suggestions import update_clusters

class ProductView(View):
    def get(self,request):
        if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
            
            user_reviews = Comment.objects.filter(user_name=request.user.username).prefetch_related('product')
            user_reviews_product_ids = set(map(lambda x: x.product.id, user_reviews))

            try:
                user_cluster_name = \
                    User.objects.get(username=request.user.username).cluster_set.first().name
            except:
                update_clusters(is_new_user=True)
                user_cluster_name = \
                    User.objects.get(username=request.user.username).cluster_set.first().name
            
            user_cluster_other_members = \
                Cluster.objects.get(name=user_cluster_name).users \
                    .exclude(username=request.user.username).all()
            other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

            other_users_reviews = \
                Comment.objects.filter(user_name__in=other_members_usernames) \
                    .exclude(product__id__in=user_reviews_product_ids)
            other_users_reviews_product_ids = set(map(lambda x: x.product.id, other_users_reviews))
                    
            product_list = sorted(
                list(Product.objects.filter(id__in=other_users_reviews_product_ids)),
                key=lambda x: x.average_rating(),
                reverse=True
            )
        else:
            cartItems=0
        cosmetics = Product.objects.filter(category='C')
        petproducts = Product.objects.filter(category="PP")
        product_data = Product.objects.all()
        if request.user.is_authenticated:
            return render(request, 'app/home.html',{
                'cosmetics':cosmetics,'recommended_list': product_list,'petproducts':petproducts,'cartItems':cartItems,'username': request.user.username,'product_data':product_data,
                })
        else:
            return render(request, 'app/home.html',{
                'cosmetics':cosmetics,'petproducts':petproducts,'cartItems':cartItems,'username': request.user.username,'product_data':product_data,
                })

class ProductDetailView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
        else:
            cartItems = 0
        product = Product.objects.get(pk=pk)
        related_product = Product.objects.filter(category = product.category).exclude(pk = pk)
        form = CommentForm()
        comment = Comment.objects.all().filter(product = product.id)
        product_data = Product.objects.all()
        in_cart = False
        in_wishlist = False 
        if request.user.is_authenticated:
            in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            in_wishlist = Wishlist.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            user_reviews = Comment.objects.filter(user_name=request.user.username).prefetch_related('product')
            user_reviews_product_ids = set(map(lambda x: x.product.id, user_reviews))

            try:
                user_cluster_name = \
                    User.objects.get(username=request.user.username).cluster_set.first().name
            except:
                update_clusters(is_new_user=True)
                user_cluster_name = \
                    User.objects.get(username=request.user.username).cluster_set.first().name
            
            user_cluster_other_members = \
                Cluster.objects.get(name=user_cluster_name).users \
                    .exclude(username=request.user.username).all()
            other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

            other_users_reviews = \
                Comment.objects.filter(user_name__in=other_members_usernames) \
                    .exclude(product__id__in=user_reviews_product_ids)
            other_users_reviews_product_ids = set(map(lambda x: x.product.id, other_users_reviews))
                    
            product_list = sorted(
                list(Product.objects.filter(id__in=other_users_reviews_product_ids)),
                key=lambda x: x.average_rating(),
                reverse=True
            )
            discountpercent = ((int(product.selling_price)-int(product.discounted_price)) / int(product.selling_price))*100
            return render(request,'app/productdetail.html',{
                'comment':comment,'form':form,'product':product,'discountpercent':discountpercent,'cartItems':cartItems,'incart':in_cart,'inwishlist':in_wishlist,'related_product':related_product,'recommended_list':product_list,
                'product_data':product_data,
                })
        else:
            discountpercent = ((int(product.selling_price)-int(product.discounted_price)) / int(product.selling_price))*100
            return render(request,'app/productdetail.html',{
                'comment':comment,'form':form,'product':product,'discountpercent':discountpercent,'cartItems':cartItems,'incart':in_cart,'inwishlist':in_wishlist,'related_product':related_product,
                'product_data':product_data,
                })

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
        else:
            cartItems = 0
        form = CustomerProfileForm()
        product_data = Product.objects.all()
        gender = request.user.profile.gender
        if gender =='Male':
            return render(request,'app/profile.html',{'form':form,'Male':gender, 'active':'btn-primary','cartItems':cartItems,'product_data':product_data,})
        elif gender == 'Female':
            return render(request,'app/profile.html',{'form':form,'Female':gender, 'active':'btn-primary','cartItems':cartItems,'product_data':product_data,})
        else:
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary','cartItems':cartItems,'product_data':product_data,})

@login_required
def address(request):
    if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
    else:
        cartItems = 0
    add = Customer.objects.filter(user=request.user)
    product_data = Product.objects.all()
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary',"cartItems":cartItems,'product_data':product_data,})
@login_required
def orders(request):
    if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
    op = OrderPlaced.objects.filter(user=request.user)
    product_data = Product.objects.all()
    context = {"cartItems":cartItems,'order_placed':op,'product_data':product_data,}
    return render(request, 'app/orders.html',context)

def change_password(request):
 return render(request, 'app/changepassword.html')

def cosmetics(request,data=None):
    if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
    else:
        cartItems = 0
    product_data = Product.objects.all()
    if data ==None:
        cosmetics = Product.objects.filter(category='C')
    elif data == "Loreal" or data =="Lakme" or data == "Biotique":
        cosmetics=Product.objects.filter(category='C').filter(brand=data)
    elif data == "Face_Wash":
        cosmetics=Product.objects.filter(category='C').filter(sub_category=data)
    elif data == "below":
        cosmetics=Product.objects.filter(category='C').filter(discounted_price__lt=1000)
    elif data == "above":
        cosmetics=Product.objects.filter(category='C').filter(discounted_price__gt=1000)
    return render(request, 'app/cosmetics.html',{'cosmetics':cosmetics,"cartItems":cartItems,'product_data':product_data,})

def petproducts(request,data=None):
    if request.user.is_authenticated:
            user = request.user
            cartItems=0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    cartItems += p.quantity
            else:
                cartItems = 0
    else:
        cartItems = 0
    product_data = Product.objects.all()
    if data ==None:
        petproducts = Product.objects.filter(category='PP')
    elif data == "Pedigree" or data =="Royal_Canin" or data == "Drools":
        petproducts = Product.objects.filter(category='PP').filter(brand=data)
    elif data == "Pet_Utensils":
        petproducts=Product.objects.filter(category='PP').filter(sub_category=data)
    elif data == "below":
        petproducts=Product.objects.filter(category='PP').filter(discounted_price__lt=1000)
    elif data == "above":
        petproducts=Product.objects.filter(category='PP').filter(discounted_price__gt=1000)
    return render(request, 'app/petproducts.html',{'petproducts':petproducts,'product_data':product_data,})
def signup(request):
    if request.method == "POST":
        get_otp = request.POST.get('otp')
        if get_otp:
            get_user = request.POST.get('user')
            user = User.objects.get(username=get_user)
            if int(get_otp) == UserOtp.objects.filter(user=user).last().otp:
                user.is_active=True
                user.save()
                messages.success(request, "Congratulations!! Registered Successfully")
                return redirect('login')
            else:
                messages.warning(request, f"Wrong Otp")
                return render(request,'app/signup.html',{'otp':True,'user':user})     
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() 
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.phone_num = form.cleaned_data.get('phone_num')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.profile_pic = form.cleaned_data.get('profile_pic')
            user.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            user_otp = random.randint(100000,999999)
            UserOtp.objects.create(user=user,otp=user_otp)
            mess = f"Hello {user.first_name},\nYour Otp is {user_otp}\n\n\nRegards,\nAndocs"

            send_mail(
                "Welcome to Andocs - Verify Your Email",
                 mess, 
                 settings.EMAIL_HOST_USER, 
                 [user.email],
                 fail_silently=False
                 )
            return render(request,'app/signup.html',{'otp':True,'user':user})
    else:
        form = SignUpForm()
    return render(request,'app/signup.html',{'form':form})
@login_required
def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart= Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        cartItems=0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                cartItems += p.quantity
                shipping_amount = 70.0
                amount += tempamount
            totalamount = amount + shipping_amount
        else:
            amount = 0
            shipping_amount = 0
            totalamount = 0
    product_data = Product.objects.all()
    context = {'carts':cart,'totalamount':totalamount,'shippingamount':shipping_amount,'amount':amount,'cartItems':cartItems,
                'product_data':product_data}
    return render(request, 'app/cart.html',context)
@login_required
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        add = Customer.objects.filter(user=user)
        cart= Cart.objects.filter(user=user)
        amount = 0.0
        total_amount = 0.0
        totalamount = 0
        cartItems=0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                cartItems += p.quantity
                shipping_amount = 70.0
                amount += tempamount
            totalamount = amount + shipping_amount
        else:
            amount = 0
            shipping_amount = 0
            totalamount = 0
    product_data = Product.objects.all()
    context = {'carts':cart,'totalamount':totalamount,'shippingamount':shipping_amount,'amount':amount,'cartItems':cartItems,'add':add,
                'product_data':product_data}
    return render(request, 'app/checkout.html',context)
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity = c.quantity).save()
        c.delete()
    return redirect("orders")
@login_required
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:', productId)

    user = request.user
    print(user)
    product = Product.objects.get(id = productId)
    print(product)
    cart, created = Cart.objects.get_or_create(user=user,product = product)

    if action == 'add':
        cart.quantity = (cart.quantity + 1)
    elif action == 'remove':
        cart.quantity = (cart.quantity - 1)
    elif action == 'delete':
        cart.quantity = 0
        

    cart.save()

    if cart.quantity <= 0:
        cart.delete()

    return JsonResponse("Item was added!",safe=False)


def aboutus(request):
    return render(request,'app/aboutus.html/')

@login_required
def add_address(request):
    if request.user.is_authenticated:
        user = request.user
        cartItems=0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                cartItems += p.quantity
        else:
            cartItems = 0
    else:
        cartItems = 0
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
        usr = request.user
        name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']
        mobile_number = form.cleaned_data['mobile_number']
        reg = Customer(user = usr,name = name,locality=locality,city=city,state=state,zipcode=zipcode,mobile_number=mobile_number)
        reg.save()
        messages.success(request, "Address added successfully.")
        return redirect('address')
    return render(request,'app/add_address.html',{'form':form,'active':'btn-primary','cartItems':cartItems})

def resend_otp(request):
    if request.method == "GET":
        get_user = request.GET['user']
        if User.objects.filter(username=get_user).exists() and not User.objects.get(username=get_user).is_active:
            user =  User.objects.get(username=get_user)
            user_otp = random.randint(100000,999999)
            UserOtp.objects.create(user=user,otp=user_otp)
            mess = f"Hello {user.first_name},\n\nYour Otp is {user_otp}\n\n\nRegards,\nAndocs"

            send_mail(
                "Welcome to Andocs - Verify Your Email",
                 mess, 
                 settings.EMAIL_HOST_USER, 
                 [user.email],
                 fail_silently=False
                 )
            return HttpResponse("Resend")
    return HttpResponse("Can't Send")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
                get_user = request.POST.get('user')
                user = User.objects.get(username=get_user)
                if int(get_otp) == UserOtp.objects.filter(user=user).last().otp:
                    user.is_active=True
                    user.save()
                    login(request, user)
                    return redirect('home')
                else:
                    messages.warning(request, f"Wrong Otp")
                    return render(request,'app/login.html',{'otp':True,'user':user})

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        elif not User.objects.filter(username=username).exists():
            messages.success(request, f"Please enter a correct username and password. Note that both fields may be case-sensitive.")
            return redirect('login')
        elif not User.objects.get(username=username).is_active:
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            user_otp = random.randint(100000,999999)
            UserOtp.objects.create(user=user,otp=user_otp)
            mess = f"Hello {user.first_name},\n\nYour Otp is {user_otp}\n\n\nRegards,\nAndocs"

            send_mail(
                "Welcome to Andocs - Verify Your Email",
                 mess, 
                 settings.EMAIL_HOST_USER, 
                 [user.email],
                 fail_silently=False
                 )
            return render(request, 'app/login.html',{'otp':True,'user':user})
        else:
            messages.success(request, f"Please enter a correct username and password. Note that both fields may be case-sensitive.")
            return redirect('login')

    form = AuthenticationForm()
    return render(request, 'app/login.html',{'form':form})

def search(request):
    query = request.GET['query']
    if len(query)>78:
        products = Product.objects.none()
    else:
        productsTitle = Product.objects.filter(title__icontains=query)
        productsDescription = Product.objects.filter(description__icontains=query)
        products = productsTitle.union(productsDescription)
    if products.count() == 0:
        messages.warning(request,"No search results found. Please refine your query.")
    return render(request,'app/search.html',{'products':products,'query':query})

def contacts(request):
    return render(request,'app/contactus.html')

def helpdesk(request):
    return render(request,'app/helpdesk.html')

@login_required
def deleteAddress(request):
    data = json.loads(request.body)
    addressId = data['addressId']
    action = data['action']

    print('Action:',action)
    print('addressId:', addressId)

    user = request.user
    print(user)
    address = Customer.objects.get(id = addressId)
    print(address)
    if action == 'delete':
        address.delete()
    return JsonResponse("Address deleted successfully!",safe=False)

@login_required
def editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = UserProfileUpdateForm(request.POST,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': u_form,
        'p_form':p_form
    }
    return render(request,'app/edit_profile.html',context)


@login_required
def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist= Wishlist.objects.filter(user=user)
        cartItems=0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                cartItems += p.quantity
        else:
            cartItems = 0
    else:
        cartItems = 0
    return render(request,'app/wishlist.html',{'wishlists':wishlist,'cartItems':cartItems})

@login_required
def updateWishlist(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:',action)
    print('productId:', productId)

    user = request.user
    print(user)
    product = Product.objects.get(id = productId)
    print(product)
    wishlist, created = Wishlist.objects.get_or_create(user=user,product = product)

    if action == 'add':
        wishlist.quantity = (wishlist.quantity + 1)
    elif action == 'remove':
        wishlist.quantity = (wishlist.quantity - 1)
    elif action == 'delete':
        wishlist.quantity = 0
        

    wishlist.save()

    if wishlist.quantity <= 0:
        wishlist.delete()

    return JsonResponse("Item was added!",safe=False)

def team(request):
    return render (request,'app/team.html')

def services(request):
    return render(request,'app/services.html')

@login_required
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.user_name = request.user.username
            data.rating = form.cleaned_data['rating']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            update_clusters(is_new_user=False)
            messages.success(request,"Your review has been sent. Thank you for your Interest.")
            return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
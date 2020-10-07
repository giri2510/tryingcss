import itertools
import json
import logging
import smtplib
from datetime import timezone
from math import ceil
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, UserManager, AbstractUser, AnonymousUser, PermissionManager
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.timezone import now
from .models import Customer, Contact
from store.models import Product, Order, Merchentdb, Orderitem  # ,Orderupdate, Statuscheck
import logging
from django.core.mail import BadHeaderError, send_mail

logger = logging.getLogger(__name__)


def home(request):
    # user creation
    if request.method == 'POST':
        username = request.POST['custusername']
        firstname = request.POST['custfirstname']
        lastname = request.POST['custlastname']
        email = request.POST['custemail']
        password1 = request.POST['custpassword1']
        password2 = request.POST['custpassword2']
        # create user
        SpecialSym = ['$', '@', '#', '%']
        if password1 != password2:
            messages.error(request, 'Password  Not Matching Please Try Again')
            return redirect("/customer/")
        else:
            if not User.objects.filter(username=username).exists():
                myuser = User.objects.create_user(username=username, email=email, password=password1)
                myuser.first_name = firstname
                myuser.last_name = lastname
                messages.success(request, "Your account has been created ")
                logger.warning("Customer signup success(home())")
                return redirect("/customer/")
            else:
                messages.error(request, "Username already exist")
                logger.warning("Customer signup error(home())")
                return redirect("/customer/")
    else:
        return redirect(request, "customer/error.html")


def custlogin(request):
    if request.method == 'POST':
        username = request.POST["custlogin"]
        password = request.POST["custpsw"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successed")
            logger.warning("Customer Login success(custlogin())")
            return redirect("/customer/")
        else:

            messages.error(request, "Invalid Username and Password")
            logger.warning("Customer Login error(custlogin())")
            return redirect("/customer/")
    return redirect(request, "customer/error.html")


@login_required
def custlogout(request):
    logout(request)
    messages.success(request, "Logout Successfully ")
    logger.warning("Customer Logout (custlogout())")
    return redirect('/customer')


def index(request):
    allproducts = []
    prodcateg = Product.objects.values('prod_category', 'prod_id')
    cats = {item['prod_category'] for item in prodcateg}

    for cat in cats:
        prod = Product.objects.filter(prod_category=cat, prod_status='added')

        n = len(prodcateg)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allproducts.append([prod, range(1, nslides), nslides])
    # params={'no_of_slides':nslides,'range':range(1,nslides),'product':products}
    # allprod=[[products,range(1,nslides),nslides],
    #       [products,range(1,nslides),n],[products,range(1,nslides),nslides],
    #      [products,range(1,nslides),n],[products,range(1,nslides),nslides],
    #     [products,range(1,nslides),n]]

    params = {'allproducts': allproducts}
    logger.warning("Product shows to customer(index())")
    return render(request, "customer/products.html", params)


def category(request, slug):
    prod = Product.objects.filter(prod_category=slug, prod_status='added')
    print("prod", prod)
    context = {'prod': prod}
    return render(request, 'customer/category.html', context)


def loginerror(request):
    user = request.user
    if user.is_authenticated:
        return redirect(request, "customer/home")
    else:
        return render(request, "customer/error.html")


@login_required(login_url='error')
def checkout(request):
    js = []
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        items_json = request.POST.get('itemsJson', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        js.append(items_json)
        order = Order.objects.get_or_create(name=name, email=email, person=request.user, phone=phone,
                                            address=address, city=city, state=state, zip_code=zip_code,
                                            order_completed=False)
        for k in js:
            l = json.loads(k)
            for i in l:
                ad = i[2]
                af = l[i][0]
                item = get_object_or_404(Product, prod_id=ad)
                order_qs = Order.objects.filter(person=request.user, name=name, order_completed=False).order_by(
                    'date_created')
                if order_qs.exists():
                    order = order_qs[0]
                    if order.items.filter(item=item, status="Order has been placed").exists():
                        messages.error(request,
                                       "This item is already placed. !!!If you want to purchase it then try different "
                                       "Name")
                        logger.warning("checking user is present or not")
                        return redirect("home")


                    else:

                        order_item, created = Orderitem.objects.get_or_create(item=item, email=email,
                                                                              cust_order=request.user,
                                                                              quantity=af,
                                                                              status="Order has been placed")

                        order.items.add(order_item)
                        logger.warning("checking user is present then add to cart")
                        messages.info(request, "This item was added to your cart.")

                else:

                    order_item, created = Orderitem.objects.get_or_create(item=item, email=email,
                                                                          cust_order=request.user,
                                                                          quantity=af, status="Order has been placed")
                    logger.warning("checking user is present or not availabe then create new and add cart")
                    order.items.add(order_item)
                    messages.info(request, "This item was added to your cart.")
        subject = 'Order has been placed.'
        message = f'Order Id is :'+''+str(order.id)+'\n\nYour E-mail id is :'+''+str(email)+'\n\n Goto :- http://127.0.0.1:8000/customer/tracker/'+'\n To check your order status.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)

        id = order.id
        thank = True

        logger.warning("Checkout feeling delivery details and adding items to cart(checckout())")
        return render(request, 'customer/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'customer/checkout.html')  # , {'thank': thank})


@login_required(login_url='error')
def tracker(request):
    tracker = []
    itmpr = []
    stat = []
    iterator = itertools.count()
    if request.method == 'POST':
        orderid = request.POST.get('orderid')
        email = request.POST.get('email')
        if Order.objects.filter(id=orderid, email=email, person=request.user).exists():
            tracking = Order.objects.filter(id=orderid, email=email, person=request.user)
            tracking1 = tracking[0].id
            print("tracking", tracking1)
            mulitems = Orderitem.objects.filter(cust_order_id=request.user).order_by('date_created')

            for i in mulitems:
                if request.user == i.item.owner:
                    if i.item.discount_price:
                        rsqty = i.item.discount_price * i.quantity
                        itmpr.append(rsqty)
                    else:
                        nonrsty = i.item.prod_price * i.quantity
                        itmpr.append(nonrsty)
            total = 0
            for j in itmpr:
                total = total + j
            logger.warning("Product Tracking order (tracking())")
            return render(request, 'customer/tracker.html',
                          {'tracking': tracking, 'mulitems': mulitems, 'total': total})
        else:
            logger.warning("Product Tracking order not found (tracking())")
            return HttpResponse('Order not found')

        # items=Orderitem.objects.filter(cust_order_id=track.person).order_by('date_created')
        # print("items",items)

    return render(request, 'customer/tracker.html')  # , {'track': tracker})


def productview(request, myid):
    product = Product.objects.filter(prod_id=myid, prod_status='added')
    asd = product[0]
    relate = Product.objects.filter(prod_category=asd.prod_category, prod_status='added')
    logger.warning("Silgle product view by product id(productview())")
    return render(request, 'customer/productview.html', {'product': product[0], 'relate': relate})


def search(request):
    logger.warning("Search product (search())")
    return render(request, 'customer/search.html')


@login_required(login_url='error')
def kirana(request):
    allproducts = []
    prodcateg = Product.objects.values('ownerprod', 'prod_id')
    print("prodcateg", prodcateg)
    cats = {item['ownerprod'] for item in prodcateg}
    for cat in cats:
        prod = Product.objects.filter(ownerprod=cat, prod_status='added')
        allproducts.append([prod, range(0, 7)])
    mert = Merchentdb.objects.all()
    print("mert", mert)
    params = {'allproducts': allproducts, 'mert': mert}

    return render(request, 'customer/kirana.html', params)


@login_required(login_url='error')
def kirana_store(request, myid):
    prods = Product.objects.filter(ownerprod=myid, prod_status='added')

    return render(request, 'customer/kiranastoree.html', {'prods': prods})


@login_required(login_url='error')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, "Your query has been submited successfully")
        thank = True
        logger.warning("Customer contacting with us (contact())")
        return render(request, 'customer/contact.html', {'thank': thank})
    return render(request, 'customer/contact.html')


def userlogout(request):
    logout(request)
    logger.warning("Customer Logout(userlogout())")
    messages.success(request, "Logout Successfully ")
    return redirect('home')

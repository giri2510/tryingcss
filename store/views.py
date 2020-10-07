from math import ceil
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, UserManager, AbstractUser, AnonymousUser, PermissionManager
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
import logging

logger = logging.getLogger(__name__)

# Create your views here.

from .models import Merchentdb, Product, Orderitem, Finalorder, Order  # , Orderupdate,Statuscheck


def index(request):
    return render(request, 'store/home.html')


def userregister(request):
    if not Merchentdb.objects.filter(merch_name=request.user).exists():
        if request.method == 'POST':
            name = request.user
            reggno = request.POST.get('regno', '')
            shopname = request.POST.get('shopname', '')
            address1 = request.POST.get('address1', '') + " " + request.POST.get('landmark', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip', '')
            phone = request.POST.get('phone', '')
            commit = Merchentdb(merch_reggno=reggno, merch_name=name, merch_shop=shopname, merch_address=address1,
                                merch_phone=phone, merch_city=city, merch_state=state, merch_zip=zip_code, )
            commit.save()
            messages.success(request, "Details Added")
            logger.warning("************ Registrations Success (def userregister) ************")
            return redirect("home")
    else:
        messages.error(request, "Data already exist")
        logger.warning("************ Registrations Problem (def userregister)************")
        return redirect("home")
    return render(request, "store/index.html")


def usersignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # create user
        if password1 != password2:
            messages.error(request, 'Password  Not Matching Please Try Again')
            return redirect('home')


        else:
            if not User.objects.filter(username=username).exists():
                myuser = User.objects.create_user(username=username, email=email, password=password1, is_staff=True)
                myuser.first_name = firstname
                myuser.last_name = lastname
                # myuser.user_permissions.set(['sotre.add_product','sotre.view_product','store.delete_product','store.change_product'])
                permission1 = Permission.objects.get(name='Can add product')
                permission2 = Permission.objects.get(name='Can view product')
                permission3 = Permission.objects.get(name='Can change product')
                permission4 = Permission.objects.get(name='Can delete product')

                myuser.user_permissions.add(permission1)
                myuser.user_permissions.add(permission2)
                myuser.user_permissions.add(permission3)
                myuser.user_permissions.add(permission4)
                myuser.save()
                messages.success(request, "Your account has been created ")
                return redirect("home")
            else:
                messages.error(request, "Username already exist")
                return redirect("home")
    else:
        return HttpResponse('404 Not Found please try again')


def userlogin(request):
    if request.method == 'POST':
        username = request.POST["loginusername"]
        password = request.POST["psw"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successed")
            logger.info("Loging (userlogin)")
            return redirect("home")
        else:
            messages.error(request, "Invalid Username and Password")
            logger.warning("Loging error (userlogin)")
            return redirect("home")
    return HttpResponse("Please login")


@login_required
@permission_required('store.add_product', login_url='/store/')
def addproduct(request):
    if request.method == 'POST':
        prodname = request.POST.get('prodname', '')
        category = request.POST.get('category', '')
        subcategory = request.POST.get('subcategory', '')
        price = request.POST.get('price', '')
        desc = request.POST.get('desc', '')
        images = request.FILES['image']
        discount_price = request.POST.get('discountprice')
        date = request.POST.get('updatedate', '')
        prod = Product(prod_name=prodname, owner=request.user,
                       ownerprod=Merchentdb.objects.get(merch_name=request.user),
                       prod_category=category, prod_subcategory=subcategory,
                       prod_desc=desc, prod_price=price, discount_price=discount_price, image=images, date=date)
        prod.save()
        messages.success(request, "Product Added Successfully")
        logger.info("Product Adding (def addproduct())")
        return render(request, 'store/addproduct.html')
    logger.warning("Product Adding (def addproduct())")
    return render(request, 'store/addproduct.html')


@login_required
@permission_required('store.view_product', login_url='/store/')
def productview(request):
    allprod = []
    prodcateg = Product.objects.values('prod_category', 'prod_id')
    cats = {item['prod_category'] for item in prodcateg}
    for cat in cats:
        prod = Product.objects.filter(prod_category=cat, owner=request.user,prod_status='added')
        allprod.append([prod, range(0, 7)])
    # Pagging
    paginator = Paginator(allprod, 8)  # So limited to 5 profiles in a page

    page = request.GET.get('page')
    profile = paginator.get_page(page)
    print("profile", profile)
    params = {'allprod': profile}
    logger.warning("Product view(productview())")
    return render(request, 'store/productviews.html', params)


@login_required
@permission_required('store.change_product', login_url='/store/')
def produpdate(request, myid):
    product = Product.objects.filter(prod_id=myid,prod_status='added')
    if request.method == 'POST':
        prodname = request.POST.get('updateprodname', '')
        category = request.POST.get('updatecategory', '')
        subcategory = request.POST.get('updatesubcategory', '')
        price = request.POST.get('updateprice', '')
        desc = request.POST.get('updatedesc', '')
        discount_price = request.POST.get('updatediscountprice', '')
        date = request.POST.get('uppdate', '')
        Product.objects.filter(prod_id=myid,prod_status='added').update(prod_name=prodname,
                                                    prod_category=category, prod_subcategory=subcategory,
                                                    prod_desc=desc, prod_price=price, discount_price=discount_price,
                                                    date=date)
        if request.method == 'POST' and request.FILES:
            m = Product.objects.get(prod_id=myid,prod_status='added')
            images = request.FILES['updateimage']
            m.image = images
            m.save()
            messages.success(request, "Product has been updated successfully")
            return redirect('productviews')
        messages.success(request, "Product has been updated successfully")
        logger.error("Product Updation(produpdate())")
        return redirect('productviews')
    logger.error("Product Updation(produpdate())")
    return render(request, 'store/produpdate.html', {'product': product[0]})


@login_required
@permission_required('store.delete_product', login_url='/store/')
def prodelete(request, myid):
    Product.objects.filter(prod_id=myid).update(prod_status='deleted')
    messages.success(request, 'Product has been removed form DATABASE')
    #product.delete()
    logger.warning("Product Updation(proddelete())")
    return redirect('productviews')


@login_required
def userlogout(request):
    logout(request)
    messages.success(request, "Logout Successfully ")
    logger.warning("Logout(userlogout())")
    return redirect('home')


@login_required
def orders(request):
    allown = []
    asd = Order.objects.filter(items__item__owner=request.user,order_completed=False).distinct().order_by('-date_created', '-id')
    allown.append(asd)
    # Pagging
    paginator = Paginator(asd,4)  # So limited to 5 profiles in a page

    page = request.GET.get('page')


    profile = paginator.get_page(page)  # data

    params = {'allown': allown,'asd':profile}
    logger.warning("Checking orders at merchent side(orders())")
    return render(request, 'store/orders.html', params)

@login_required
def ordershistory(request):
    allown = []
    asd = Order.objects.filter(items__item__owner=request.user,order_completed=True).distinct().order_by('-date_created', '-id')
    allown.append(asd)
    # Pagging
    paginator = Paginator(asd,4)  # So limited to 5 profiles in a page

    page = request.GET.get('page')


    profile = paginator.get_page(page)  # data

    params = {'allown': allown,'asd':profile}
    logger.warning("Checking orders at merchent side(orders())")
    return render(request, 'store/orderhistory.html', params)

def post_by_tag(request, myid):
    itmpr = []
    stat=[]
    cust = Order.objects.get(pk=myid)
    mulitems = Orderitem.objects.filter(cust_order_id=cust.person_id).order_by('-date_created')
    """for i in mulitems:
        if request.user == i.item.owner:
            if i.item.discount_price:
                rsqty = i.item.discount_price * i.quantity
                itmpr.append(rsqty)
            else:
                nonrsty = i.item.prod_price * i.quantity
                itmpr.append(nonrsty)"""
    """for k in cust.items.all():
        if request.user == k.item.owner:
            if k.item.discount_price:
                rsqty = k.item.discount_price * k.quantity
                itmpr.append(rsqty)
            else:
                nonrsty = k.item.prod_price * k.quantity
                itmpr.append(nonrsty)"""
    for j in cust.items.all():
        stat.append(j.status)
        print("iii",j.status)
    #print("stat", stat)
    if 'Order Accepted' in stat:
        print("Order Pending")
        Order.objects.filter(pk=myid).update(order_completed=False)
    elif 'Order has been placed' in stat:
        print("order pending")
        Order.objects.filter(pk=myid).update(order_completed=False)
    elif 'Ready to Deliever' in stat:
        print("Order Pending")
        Order.objects.filter(pk=myid).update(order_completed=False)
    elif 'Ontheway' in stat:
        print("Order Pending")
        Order.objects.filter(pk=myid).update(order_completed=False)
    elif 'Order Placed' in stat:
        print("Order Pending")
        Order.objects.filter(pk=myid).update(order_completed=False)
    else:
        Order.objects.filter(pk=myid).update(order_completed=True)
        print("completed")



    total = 0
    for j in itmpr:
        total = total + j

    context = {'cust': cust, 'mulitems': mulitems, 'total': total}  # ,'orde':orde}
    logger.warning("Checking orders at merchent side ID's Wise(orders())")
    return render(request, 'store/post_by_tag.html', context)

def bill(request,myid):
    itmpr = []
    stat = []
    cust = Order.objects.get(pk=myid)
    for k in cust.items.all():
        if request.user == k.item.owner:
            if k.item.discount_price:
                rsqty = k.item.discount_price * k.quantity
                itmpr.append(rsqty)
            else:
                nonrsty = k.item.prod_price * k.quantity
                itmpr.append(nonrsty)
    total = 0
    for j in itmpr:
        total = total + j
    context = {'cust': cust, 'total': total}
    return render(request,'store/bill.html',context )

def update_status(request, myid):
    orders = Orderitem.objects.filter(id=myid)
    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        ordering = orders[0]
        if Orderitem.objects.filter(id=myid, status=status).exists():
            messages.error(request, "Already Updated")
            print("updated")
        else:
            Orderitem.objects.filter(id=myid).update(status=status)
            print("status added")

    return render(request, 'store/status_item.html', {'orders': orders})

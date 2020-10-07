from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='home'),
    path('post_by_tag/<int:myid>', views.post_by_tag, name='post_by_tag'),
    path('usersignup/',views.usersignup,name='usersignup'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('userregister/', views.userregister, name='userregister'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productviews/', views.productview, name='productviews'),
    path('produpdate/<int:myid>', views.produpdate, name='produpdate'),
    path('prodelete/<int:myid>', views.prodelete, name='prodelete'),
    path('orders/', views.orders, name='orders'),
    path('ordershistory/', views.ordershistory, name='ordersHistory'),
    path('status/<int:myid>', views.update_status, name='Updatestatus'),
    path('bill/<int:myid>', views.bill, name='Billing'),
    path('userlogout/',views.userlogout,name='userlogout'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




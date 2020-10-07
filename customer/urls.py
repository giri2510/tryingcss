from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='home'),
    path('home/',views.home,name='homeMain'),
    path('custlogin/',views.custlogin,name='custlogin'),
    path('custlogout/',views.custlogout,name='custlogout'),
    path('error/',views.loginerror,name='error'),
    path('checkout/',views.checkout,name='checkout'),
    path('kirana/',views.kirana,name='kirana'),
    path('productview/<int:myid>',views.productview,name='productview'),
    path('category/<str:slug>',views.category,name='Categoryvice'),
    path('tracker/',views.tracker,name='tracker'),
    path("search/", views.search, name="Search"),
    path("contact/", views.contact, name="Contact"),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('store_kirana/<int:myid>', views.kirana_store, name='KiranaStore'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
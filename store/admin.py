from django.contrib import admin
from .models import Merchentdb,Product,Order,Orderitem,Finalorder#,Statuscheck,Orderupdate
# Register your models here.
admin.site.register((Merchentdb,Product))
admin.site.register((Order,Orderitem))
admin.site.register(Finalorder)
#admin.site.register((Orderupdate,Statuscheck))


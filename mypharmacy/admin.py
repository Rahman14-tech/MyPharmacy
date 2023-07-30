from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(Dikelompokkan)
admin.site.register(Balance)
admin.site.register(Transaksi)
admin.site.register(Detailpenjualan)
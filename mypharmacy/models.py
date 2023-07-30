from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Customer(AbstractUser):
    no_hp = models.CharField(max_length = 100)
    
class Category(models.Model):
    category = models.CharField(max_length = 100)
    
class Medicine(models.Model):
    nama_obat = models.CharField(max_length = 100)
    stock = models.IntegerField()
    deskripsi = models.TextField()
    exp = models.DateField()
    harga_satuan = models.IntegerField()
    gambar_obat = models.FileField(upload_to = 'mypharmacy/gambarobat/')
    
    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)
        
class Dikelompokkan(models.Model):
    id_med = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    id_cat = models.ForeignKey(Category,on_delete=models.CASCADE)
    
class Balance(models.Model):
    id_cust = models.ForeignKey(Customer,on_delete=models.CASCADE)
    saldo = models.IntegerField()

class History(models.Model):
    id_cust = models.ForeignKey(Customer, on_delete=models.CASCADE)
    id_topup =  models.ForeignKey(Balance, on_delete=models.CASCADE)
    tanggal = models.DateField()
    total = models.IntegerField()
    
class Transaksi(models.Model):
    id_cust = models.ForeignKey(Customer,on_delete=models.CASCADE)
    tgl_transaksi = models.DateField()
    total_harga = models.IntegerField()
    selesai_transaksi = models.BooleanField()
    
class Detailpenjualan(models.Model):
    id_trans = models.ForeignKey(Transaksi,on_delete=models.CASCADE)
    id_med = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    qty = models.IntegerField()
    diskon = models.FloatField()
    subtotal = models.IntegerField()
    def serialize(self):
        return{
            "propertyId":self.id,
            "subtotal":self.subtotal
        }
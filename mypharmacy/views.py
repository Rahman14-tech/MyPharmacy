from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from datetime import date
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

today = date.today()


from .models import *
# Create your views here.
def logout_place(request):
    logout(request)
    return HttpResponseRedirect(reverse("loginplace"))
def loginplace(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:   
            login(request, user)
            return HttpResponseRedirect(reverse("home")) 
        else:
             return render(request, "mypharmacy/login.html", {
                "error": "Invalid username and/or password."
            }) 
    else:
        return render(request,"mypharmacy/login.html")
def home(request):
    user = Customer.objects.get(id = request.user.id)
    all_category = Category.objects.all()
    if 'category' in request.GET:
        contents_cat = request.GET['category']
        Categoryobject = Category.objects.get(category = contents_cat)
        dikelom = Dikelompokkan.objects.filter(id_cat = Categoryobject)
        return render(request,"mypharmacy/home.html",{
            'user':user,
            'Category':all_category,
            'medicine':dikelom
        }) 
    return render(request,"mypharmacy/home.html",{
            'username':user.first_name,
            'Category':all_category
    })
def profile(request,email):
    user = Customer.objects.get(id = request.user.id)
    balance = Balance.objects.get(id_cust = user)
    return render(request,"mypharmacy/profile.html",{
        'user':user,
        'balance':balance
    })
def topup(request):
    if request.method == "POST":
        user = Customer.objects.get(id = request.user.id)
        newtop = request.POST['topup']
        intnewtop = int(newtop)
        if intnewtop <= 10000:
            return render(request,"mypharmacy/topup.html",{
                'error':"Minimal top up Rp. 10000"
            })
        balance = Balance.objects.get(id_cust = user)
        tempsaldo = int(balance.saldo) + intnewtop
        balance.saldo = tempsaldo
        balance.save()
        return HttpResponseRedirect(reverse("profile",kwargs={'email':user.email}))
    else:
        user = Customer.objects.get(id = request.user.id)
        balance = Balance.objects.get(id_cust = user)
        return render(request,"mypharmacy/topup.html")
@csrf_exempt
def keranjangApi(request):
    if request.method == 'PUT':
        current_user = request.user
        deletedJson = json.loads(request.body)
        deletedId = deletedJson["propertyId"]
        DetailPenjualan = Detailpenjualan.objects.get(id = deletedId)
        medicine = Medicine.objects.get(id = DetailPenjualan.id_med.id)
        medicine.stock += DetailPenjualan.qty
        Transaksisekarang = Transaksi.objects.get(id_cust = current_user, selesai_transaksi = False)
        Transaksisekarang.total_harga -= DetailPenjualan.subtotal
        Transaksisekarang.save()
        medicine.save()
        DetailPenjualan.delete()
        return JsonResponse({"success":"Success deleting an item."})
    else:
        objectTransaksi = Transaksi.objects.get(id_cust = request.user,selesai_transaksi = False)
        semuaDetailPenjualan = Detailpenjualan.objects.filter(id_trans = objectTransaksi)
        return JsonResponse([detail.serialize() for detail in semuaDetailPenjualan],safe = False)
def keranjang(request):
    if request.method == 'POST':
        current_user = request.user
        try:
            Balanceuser = Balance.objects.get(id_cust = current_user)
        except Transaksi.DoesNotExist:
            return render(request,"mypharmacy/basket.html")
        try:
            transaksiSekarang = Transaksi.objects.get(id_cust = current_user,selesai_transaksi = False)
        except Transaksi.DoesNotExist:
            return render(request,"mypharmacy/basket.html")
        try:
            details = Detailpenjualan.objects.filter(id_trans = transaksiSekarang)
        except Detailpenjualan.DoesNotExist:
            return render(request,"mypharmacy/basket.html")
        if transaksiSekarang.total_harga > Balanceuser.saldo:
            return render(request,"mypharmacy/basket.html",{
            'barang':transaksiSekarang,
            'details':details,
            'error':"Pembayaran tidak berhasil pastikan saldo anda cukup!"
        })
        Balanceuser.saldo -= transaksiSekarang.total_harga
        Balanceuser.save()
        transaksiSekarang.selesai_transaksi = True
        transaksiSekarang.save()
        return render(request,'mypharmacy/success.html',{
            'success':"Pembayaran berhasil"
        })
    else:
        current_user = request.user
        try:
            transaksiSekarang = Transaksi.objects.get(id_cust = current_user,selesai_transaksi = False)
        except Transaksi.DoesNotExist:
            return render(request,"mypharmacy/basket.html")  
        try:
            details = Detailpenjualan.objects.filter(id_trans = transaksiSekarang)
        except Detailpenjualan.DoesNotExist:
            return render(request,"mypharmacy/basket.html")
        return render(request,"mypharmacy/basket.html",{
            'barang':transaksiSekarang,
            'details':details
        })
def view(request,id_barang):
    if request.method == "POST":
        itemquantity = request.POST['itemquantity']
        barangnya = Medicine.objects.get(id = id_barang)
        barangdankategori = Dikelompokkan.objects.filter(id_med = barangnya)
        intitemquantity = int(itemquantity)
        if intitemquantity > barangnya.stock or intitemquantity <= 0:
            return render(request,"mypharmacy/view.html",{
                'Content':barangnya,
                'Category':barangdankategori,
                'error':'Tidak bisa membeli barang melebihi stock atau kurang dari 1!'
            })
        try:
            trans = Transaksi.objects.get(id_cust = request.user, selesai_transaksi = False)
        except Transaksi.DoesNotExist:
            trans = Transaksi(id_cust = request.user, tgl_transaksi = today.strftime("%Y-%m-%d"),total_harga = 0,selesai_transaksi = False)
        trans.total_harga += (barangnya.harga_satuan*intitemquantity)
        try:
            detail = Detailpenjualan.objects.get(id_trans = trans,id_med = barangnya)
        except Detailpenjualan.DoesNotExist:
            detail = Detailpenjualan(id_trans = trans, id_med = barangnya, qty = 0, diskon = 0, subtotal = 0)
        tempdetailqty = detail.qty
        tempdetailqty+= intitemquantity
        detail.qty = tempdetailqty
        newharga = (tempdetailqty*barangnya.harga_satuan)
        newharga -= int((detail.diskon/100)*newharga)
        detail.subtotal = newharga
        barangnya.stock-= intitemquantity
        trans.save()
        detail.save()
        barangnya.save()
        return render(request,"mypharmacy/view.html",{
                'Content':barangnya,
                'Category':barangdankategori,
                'success':'Barang telah dimasukkan ke keranjang'
            })
    else:
        barangnya = Medicine.objects.get(id = id_barang)
        barangdankategori = Dikelompokkan.objects.filter(id_med = barangnya)
        return render(request,"mypharmacy/view.html",{
            'Content':barangnya,
            'Category':barangdankategori
        })     
def register(request):
    if request.method == "POST":
        first_name = request.POST['front_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        no_hp = request.POST['nohp']
        if password != confirmation:
            return render(request,"mypharmacy/register.html",{
                'error':'password and confirmation not match'
            })
        try:
            user = Customer.objects.create_user(username = email,email = email,password = password,first_name = first_name,last_name = last_name,no_hp = no_hp)
            user.save()
            wallet = Balance(id_cust = user,saldo = 0)
            wallet.save()
        except IntegrityError:
            return render(request,"mypharmacy/register.html",{
                'error':'email has been registered!'
            })
        return render(request,"mypharmacy/login.html")     
    else:
         return render(request,"mypharmacy/register.html")
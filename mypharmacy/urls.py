from . import views
from django.urls import path
from django.conf.urls.static import static 
from django.conf import settings
urlpatterns = [
    path("",views.loginplace,name="loginplace"),
    path("register",views.register,name="register"),
    path("logout", views.logout_place, name="logout"),
    path("home",views.home,name="home"),
    path("profile/<str:email>",views.profile,name="profile"),
    path("topup",views.topup,name="topup"),
    path("view/<int:id_barang>",views.view,name="view"),
    path("keranjang",views.keranjang,name="keranjang"),
    path("f742cf2703e3300ef932616cd5fe0541",views.keranjangApi,name="keranjangApi"),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

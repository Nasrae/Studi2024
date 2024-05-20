from django.contrib import admin
from django.urls import path
from joapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('', views.acceuil, name='acceuil'),
    path('acceuil/', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('contact/', views.contact, name='contact'),
    path('offres/', views.offres, name='offres'),
    path('checkout/', views.checkout, name='checkout'),
    path('create_checkout_session', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),


]
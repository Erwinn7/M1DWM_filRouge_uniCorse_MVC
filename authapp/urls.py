from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Pages principales
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test/', views.test_view, name='test'),
    path('profil/', views.profil_view, name='profil'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),

    # Gestion des produits (admin)
    path('produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('produits/modifier/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'),

    # Gestion des clients (admin)
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),
    path('clients/modifier/<int:id>/', views.modifier_client, name='modifier_client'),
    path('clients/supprimer/<int:id>/', views.supprimer_client, name='supprimer_client'),
]

# Pour servir les fichiers médias (images) en développement
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

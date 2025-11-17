from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Produit, Profil
from .forms import ProduitForm, ProfilForm
from django.db.models import Q

# Test simple
def test_view(request):
    return HttpResponse("Django fonctionne ✅")

# Accueil admin
def home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(User, user_id=user_id)
    profil = get_object_or_404(Profil, user=user)
    if profil.role != 'admin':
        return redirect('client_dashboard')
    produits = Produit.objects.all()
    return render(request, 'authapp/home.html', {
        'user_login': user.user_login,
        'produits': produits
    })

# Tableau de bord client
def client_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(User, user_id=user_id)
    produits = Produit.objects.all()  # Optionnel : filtrer selon admin
    return render(request, 'authapp/client_dashboard.html', {
        'user_login': user.user_login,
        'produits': produits
    })

# Inscription (admin uniquement)
def ajouter_client(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)
    profil = get_object_or_404(Profil, user=user)
    if profil.role != 'admin':
        return redirect('home')

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        email = request.POST.get('email')
        compte_id = request.POST.get('compte_id')

        if User.objects.filter(Q(user_login=login) | Q(user_compte_id=compte_id)).exists():
            messages.error(request, "Login ou compte ID déjà utilisé.")
        else:
            new_user = User.objects.create(
                user_login=login,
                user_password=make_password(password),
                user_mail=email,
                user_compte_id=compte_id
            )
            Profil.objects.create(user=new_user, role='client')
            messages.success(request, "Client ajouté avec succès.")
            return redirect('liste_clients')

    return render(request, 'authapp/ajouter_client.html')

# Liste des clients
def liste_clients(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)
    profil = get_object_or_404(Profil, user=user)
    if profil.role != 'admin':
        return redirect('home')
    clients = User.objects.filter(profil__role='client')
    return render(request, 'authapp/liste_clients.html', {'clients': clients})

# Modifier un client
def modifier_client(request, id):
    client = get_object_or_404(User, user_id=id)
    profil = get_object_or_404(Profil, user=client)

    if request.method == 'POST':
        client.user_login = request.POST.get('login')
        client.user_mail = request.POST.get('email')

        new_password = request.POST.get('password')
        if new_password:
            client.user_password = make_password(new_password)

        client.save()

        profil.phone = request.POST.get('phone')
        profil.role = request.POST.get('role')
        profil.save()

        messages.success(request, "Client modifié.")
        return redirect('liste_clients')

    return render(request, 'authapp/modifier_client.html', {'client': client, 'profil': profil})

# Supprimer un client
def supprimer_client(request, id):
    client = get_object_or_404(User, user_id=id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, "Client supprimé.")
        return redirect('liste_clients')
    return render(request, 'authapp/supprimer_client.html', {'client': client})

# Connexion
def login_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        try:
            user = User.objects.get(user_login=login)
            if check_password(password, user.user_password):
                request.session['user_id'] = user.user_id
                profil = Profil.objects.get(user=user)
                if profil.role == 'admin':
                    return redirect('home')
                else:
                    return redirect('client_dashboard')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except User.DoesNotExist:
            messages.error(request, "Login introuvable.")
    return render(request, 'authapp/login.html')

# Déconnexion
def logout_view(request):
    request.session.flush()
    messages.info(request, "Déconnecté.")
    return redirect('login')

# Produits CRUD
def ajouter_produit(request):
    if not request.session.get('user_id'):
        return redirect('login')
    form = ProduitForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Produit ajouté.")
        return redirect('home')
    return render(request, 'authapp/ajouter.html', {'form': form})

def modifier_produit(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    produit = get_object_or_404(Produit, id=id)
    form = ProduitForm(request.POST or None, request.FILES or None, instance=produit)
    if form.is_valid():
        form.save()
        messages.success(request, "Produit modifié.")
        return redirect('home')
    return render(request, 'authapp/modifier.html', {'form': form})

def supprimer_produit(request, id):
    if not request.session.get('user_id'):
        return redirect('login')
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, "Produit supprimé.")
        return redirect('home')
    return render(request, 'authapp/supprimer.html', {'produit': produit})

# Profil personnel
def profil_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(User, user_id=user_id)
    profil, created = Profil.objects.get_or_create(user=user)
    form = ProfilForm(request.POST or None, request.FILES or None, instance=profil)
    if form.is_valid():
        form.save()
        messages.success(request, "Profil mis à jour.")
        return redirect('home')
    return render(request, 'authapp/profil.html', {'form': form})

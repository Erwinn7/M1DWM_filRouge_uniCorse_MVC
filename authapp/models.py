from django.db import models

# Ton modèle utilisateur personnalisé
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_login = models.CharField(max_length=150, unique=True)
    user_password = models.CharField(max_length=255)
    user_compte_id = models.IntegerField(unique=True)
    user_mail = models.CharField(max_length=255)
    user_date_new = models.DateTimeField(auto_now_add=True)
    user_date_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_login

# Ton modèle produit
class Produit(models.Model):
    designation_p = models.CharField(max_length=255)
    type_p = models.CharField(max_length=100)
    prix_ht = models.DecimalField(max_digits=10, decimal_places=2)
    stock_p = models.IntegerField(default=0)
    date_in = models.DateField()
    image = models.ImageField(upload_to='produits/', blank=True, null=True)

    def __str__(self):
        return self.designation_p

# Nouveau modèle profil lié à ton User
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('client', 'Client')],
        default='client'
    )

    def __str__(self):
        return f"{self.user.user_login} - {self.role}"

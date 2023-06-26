from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    prenom = models.CharField(max_length=20,null=False)
    nom = models.CharField(max_length=20,null=False)
    ville = models.CharField(max_length=20,null=False)
    pays = models.CharField(max_length=20,null=False)
    adresse = models.CharField(max_length=20,null=False)
    is_personnel = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Compte(models.Model):
    nom = models.CharField(max_length=100)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    en_attente = models.BooleanField(default=False)

    def __str__(self):
        return self.numero


class Prelevement(models.Model):
    compte_source = models.ForeignKey(Compte, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prélèvement de {self.montant} depuis le compte {self.compte_source}"


class Virement(models.Model):
    compte_source = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='virements_envoyes')
    compte_destination = models.ForeignKey(Compte, on_delete=models.CASCADE, related_name='virements_recus')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


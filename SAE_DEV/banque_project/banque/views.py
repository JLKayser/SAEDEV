from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views import View
from .models import Compte
from .models import Prelevement
from .models import Virement

def SignupClient(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        adresse = request.POST.get("adresse")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        email = request.POST.get("email")
        newclient = CustomUser(username = username, nom = nom, prenom = prenom, adresse = adresse, ville = ville, pays = pays, email= email)
        newclient.set_password(password)
        newclient.save()
        return redirect('/banque/login/client')
    else:
        return render(request, 'banque/creation_client.html')

def SignupPersonnel(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        adresse = request.POST.get("adresse")
        ville = request.POST.get("ville")
        pays = request.POST.get("pays")
        email = request.POST.get("email")
        newclient = CustomUser(username = username, nom = nom, prenom = prenom, adresse = adresse, ville = ville, pays = pays, email= email, is_personnel=True)
        newclient.set_password(password)
        newclient.save()
        return redirect('/banque/login/personnel')
    else:
        return render(request, 'banque/creation_personnel.html')

def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_personnel:
            return render(request, 'banque/dashboard_personnel.html')
        compte_source = list(Compte.objects.all().filter(client=request.user.id))
        return render(request, 'banque/dashboard.html',{'compte_source':compte_source})
    else:
        return redirect('/banque/login/client')

def supprimer_compte(request, compte_id):
    compte = Compte.objects.get(id=compte_id)
    compte.delete()
    return redirect('/dashboard')

def logoutUser(request):
    logout(request)
    return redirect('/banque/login/client')

def LoginClient(request):
    for i in list(CustomUser.objects.all()):
        print(i.password)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            print('ERREUR MDP')
            return redirect('/banque/login/client')
    else:
        return render(request, 'banque/login_client.html')

def LoginPersonnel(request):
    for i in list(CustomUser.objects.all()):
        print(i.password)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            print('ERREUR MDP')
            return redirect('/banque/login/personnel')
    else:
        return render(request, 'banque/login_personnel.html')

def depot(request):
    compte_source = list(Compte.objects.all().filter(client=request.user.id))
    return render(request,'banque/depot.html', {'compte_source':compte_source})


def prelevement(request):
    compte_source = list(Compte.objects.all().filter(client=request.user.id))
    return render(request,'banque/prelevement.html', {'compte_source':compte_source})

def virement(request):
    compte_source = list(Compte.objects.all().filter(client=request.user.id))
    compte_destination = list(Compte.objects.all().filter(client=request.user.id))
    return render(request,'banque/virement.html', {'compte_source':compte_source,'compte_destination':compte_destination})


def creation_compte(request):
    if request.method == 'POST':
        if not request.user.is_personnel:
            nom = request.POST.get("nom")
            solde = request.POST.get("solde")
            client = request.user
            new_account = Compte(nom=nom,solde=solde,client=client)
            new_account.save()
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')
    else:
        return render(request,'banque/creation_compte.html')

class TransactionValidationView(View):
    def post(self, request):
        form = TransactionValidationForm(request.POST)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            validation = form.cleaned_data['validation']
            
            compte = Compte.objects.get(pk=transaction_id)
            compte.en_attente = not validation
            compte.save()
            
            return render(request, 'dashboard.html')
        else:
            return render(request, 'dashboard.html')


class DepotView(APIView):
    def post(self, request):
        montant = float(request.POST.get('montant'))
        compte_source_id = request.POST.get('compte_source')

        compte = Compte.objects.get(pk=int(compte_source_id))
        compte.solde += int(montant)
        
        if montant > 10000:
            compte.en_attente = True
        else:
            compte.en_attente = False
        
        compte.save()

        montant_actuel = compte.solde

        context = {
            'montant_actuel': montant_actuel,
            'depot_success': True
        }
        
        return Response({'Nouveau solde': compte.solde})


class PrelevementView(APIView):
    def post(self, request):
        compte_source_id = request.POST.get('compte_source')
        montant = float(request.POST.get('montant'))

        compte = Compte.objects.get(pk=int(compte_source_id))
        compte.solde -= int(montant)
        compte.save()

        montant_actuel = compte.solde
        

        context = {
            'montant_actuel': montant_actuel,
            'depot_success': True
        }
        return Response({'Nouveau solde':compte.solde})


class VirementView(APIView):
    def post(self, request):
        compte_source_id = request.POST.get('compte_source')
        compte_destination_id = request.POST.get('compte_destination')
        montant = float(request.POST.get('montant'))

        compte_source = Compte.objects.get(pk=int(compte_source_id))
        compte_destination = Compte.objects.get(pk=int(compte_destination_id))

        compte_source.solde -= int(montant)
        compte_destination.solde += int(montant)

        compte_source.save()
        compte_destination.save()

        montant_actuel = compte_source.solde

        context = {
            'montant_actuel': montant_actuel,
            'virement_success': True
        }
        return Response({'Nouveau solde SOURCE': compte_source.solde,'Nouveau solde DESTINATION': compte_destination.solde})



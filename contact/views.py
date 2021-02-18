from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Patient
from django.contrib import messages
import pandas as pd
from django.contrib.auth.decorators import login_required
from web3 import Web3
import datetime
import hashlib
import json

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

@login_required()
def index(request):
    context = {}
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))



@login_required()
def patient_form(request):

    dt = pd.read_csv('contact/static/info/countries.txt', sep='\n')
    countries = []
    df = dt.to_dict() 
    for k, country in df.items():
        for k,v in country.items():
            countries.append(v)
    return render(request, 'patient_form.html', {'countries': countries})


@login_required()
def add_patients(request):

    ganache_url = 'http://127.0.0.1:7545'


    web3 = Web3(Web3.HTTPProvider(ganache_url))

    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"enum Contact_tracing.Statuses","name":"_status","type":"uint8"},{"internalType":"string","name":"_postal","type":"string"},{"internalType":"string","name":"_hospitalName","type":"string"},{"internalType":"string","name":"_hashing","type":"string"},{"internalType":"string","name":"_country","type":"string"}],"name":"addPatient","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPatientsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"gettPatient","outputs":[{"components":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"internalType":"struct Contact_tracing.Patient","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"patients","outputs":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"stateMutability":"view","type":"function"}]')

    address = "0xa84580e93474b942b48B16CAEeaA1920962CBd90"

    contract = web3.eth.contract(address = address, abi = abi)

    print(contract)

    if request.method == 'GET':

        precord = Patient()
        
        precord.name = request.GET.get("name")
        precord.surname = request.GET.get("surname")
        precord.address = request.GET.get("address")
        precord.email = request.GET.get("email")
        precord.city = request.GET.get("city")
        precord.region = request.GET.get("region")
        precord.postal = request.GET.get("postal")
        precord.country = request.GET.get("country")
        precord.phone = request.GET.get("phone")
        precord.status = request.GET.get("status")
        precord.notes = request.GET.get("notes", None)
        precord.created_at = request.GET.get("bdate")
        precord.user = request.user
        

        name_surname = precord.name+"_"+precord.surname
        precord.hashing = encrypt_string(name_surname)
        country = precord.country
        postal = precord.postal
        status = int(precord.status)
        
        
        result = contract.functions.addPatient(status, postal, str(precord.user), encrypt_string(name_surname), country).transact({'from':'0xF49D6960fb886B6ACD1Aca017f6306134a795457'})
        num = contract.functions.getPatientsCount().call()
        print(num)

        precord.save()

        
        

        
        
        messages.success(request, 'Record Saved')

        return render(request, 'index.html')
    else:
        return render(request, 'index.html')

@login_required()
def patients_list(request):

    patients = Patient.objects.all()  
    

    return render(request, 'patient_list.html', {'patients':patients})


@login_required
def delete_patient(request, uid):  

    ganache_url = 'http://127.0.0.1:7545'

    

    web3 = Web3(Web3.HTTPProvider(ganache_url))

    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"enum Contact_tracing.Statuses","name":"_status","type":"uint8"},{"internalType":"string","name":"_postal","type":"string"},{"internalType":"string","name":"_hospitalName","type":"string"},{"internalType":"string","name":"_hashing","type":"string"},{"internalType":"string","name":"_country","type":"string"}],"name":"addPatient","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPatientsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"gettPatient","outputs":[{"components":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"internalType":"struct Contact_tracing.Patient","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"patients","outputs":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"stateMutability":"view","type":"function"}]')
    

    address = "0xa84580e93474b942b48B16CAEeaA1920962CBd90"

    contract = web3.eth.contract(address = address, abi = abi)

    patient = Patient.objects.get(uid=uid)  
    patient.status = request.GET.get("status") 
    patient.notes = request.GET.get("notes", None)
    patient.created_at = request.GET.get("bdate")


    hashing = patient.hashing
    country = patient.country
    postal = patient.postal
    status = int(patient.status)
    

    
    result = contract.functions.addPatient(status, postal, 'deleted', str(hashing), country).transact({'from':'0xF49D6960fb886B6ACD1Aca017f6306134a795457'})
    patient.delete() 

    return redirect("http://127.0.0.1:8000/patients-list")  
    

@login_required
def update_patient_status(request, uid):  

    ganache_url = 'http://127.0.0.1:7545'

    web3 = Web3(Web3.HTTPProvider(ganache_url))

    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"enum Contact_tracing.Statuses","name":"_status","type":"uint8"},{"internalType":"string","name":"_postal","type":"string"},{"internalType":"string","name":"_hospitalName","type":"string"},{"internalType":"string","name":"_hashing","type":"string"},{"internalType":"string","name":"_country","type":"string"}],"name":"addPatient","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPatientsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"gettPatient","outputs":[{"components":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"internalType":"struct Contact_tracing.Patient","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"patients","outputs":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"stateMutability":"view","type":"function"}]')
    

    address = "0xa84580e93474b942b48B16CAEeaA1920962CBd90"

    contract = web3.eth.contract(address = address, abi = abi)

    if request.method == 'GET':
     
        patient = Patient.objects.get(uid=uid) 
        patient.status = request.GET.get("status") 
        patient.notes = request.GET.get("notes", None)
        patient.created_at = request.GET.get("bdate")


        hashing = patient.hashing
        print(patient)
        country = patient.country
        postal = patient.postal
        status = int(patient.status)

        result = contract.functions.addPatient(status, postal, str(patient.user), str(patient.hashing), country).transact({'from':'0xF49D6960fb886B6ACD1Aca017f6306134a795457'})

        patient.save()

        return redirect("http://127.0.0.1:8000/patients-list")  
    
    return redirect("http://127.0.0.1:8000/patients-list")

   
@login_required
def edit(request, uid):  
    patient = Patient.objects.get(uid=uid)  
    return render(request,'edit.html', {'patient':patient})  


def users(request):  

    dt = pd.read_csv('countries.txt', sep='\n')
    countries = []
    df = dt.to_dict() 
    for k, country in df.items():
        for k,v in country.items():
            countries.append(v)
    
    return render(request,'users.html', {'countries':countries})  


def search_results(request):

    dt = pd.read_csv('countries.txt', sep='\n')
    countries = []
    df = dt.to_dict() 
    for k, country in df.items():
        for k,v in country.items():
            countries.append(v)

    ganache_url = 'http://127.0.0.1:7545'


    web3 = Web3(Web3.HTTPProvider(ganache_url))

    abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"enum Contact_tracing.Statuses","name":"_status","type":"uint8"},{"internalType":"string","name":"_postal","type":"string"},{"internalType":"string","name":"_hospitalName","type":"string"},{"internalType":"string","name":"_hashing","type":"string"},{"internalType":"string","name":"_country","type":"string"}],"name":"addPatient","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getPatientsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"gettPatient","outputs":[{"components":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"internalType":"struct Contact_tracing.Patient","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"patients","outputs":[{"internalType":"enum Contact_tracing.Statuses","name":"status","type":"uint8"},{"internalType":"string","name":"postal","type":"string"},{"internalType":"string","name":"hospitalName","type":"string"},{"internalType":"string","name":"hashing","type":"string"},{"internalType":"string","name":"country","type":"string"}],"stateMutability":"view","type":"function"}]')
    
    address = "0xa84580e93474b942b48B16CAEeaA1920962CBd90"

    contract = web3.eth.contract(address = address, abi = abi)


    no_patients = contract.functions.getPatientsCount().call()
    
    lpatient = []
    lhash = []
    message = 'No infected people'
    if request.method == 'GET':
    
        region = request.GET.get("city")
        postal = request.GET.get("postal")
        country = request.GET.get("country")

    counter = 0
    for i in range(0, no_patients):
        patients = contract.functions.gettPatient(i).call()
        lpatient = list(patients)
        print(lpatient)
        if lpatient[0] == 0 and lpatient[1] == postal and lpatient[4] == country:
            if lpatient[3] not in lhash and lpatient[2] != 'daleted':
                lhash.append(lpatient[3])
                counter = counter + 1
            message = 'Infected people in your area are'

    
        return render(request,'infected.html', {'countries':countries, 'infected_people': counter, 'message': message})  


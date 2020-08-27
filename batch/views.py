from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CrearUserForms
from .models import *
import os
import zipfile


# Create your views here.


def blogin(request):
    '''returns the login templets'''
    if request.user.is_authenticated:
        return redirect('batch')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                print("done")
                login(request, user)
                return redirect('batch')
            else:
                messages.info(request, 'Username OR Password is Incorrect')
        # return HttpResponse("Hello, world. You're at the polls index.")
        return render(request, 'batch/login.html')


def signout(request):
    logout(request)
    return redirect('index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('batch')
    else:
        form = CrearUserForms()
        if request.method == 'POST':
            form = CrearUserForms(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('first_name')
                messages.success(request, 'Account has been Created Successfully for ' + user)
                return redirect('index')
        context = {'form': form}
        return render(request, 'batch/signup.html', context)


@login_required(login_url='index')
def batchView(request):
    '''returns the batch page templet'''
    batchs = Batch.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'batch/batch.html', {'batchs': batchs})


@login_required(login_url='index')
def pjtView(request):
    '''returns the batch page templet'''
    projects = Project.objects.filter(pcreated_by=request.user).order_by('-created_at')
    return render(request, 'batch/project.html', {'projects': projects})


@login_required(login_url='index')
def createBch(request):
    '''returns the batch page templet'''
    projects = Project.objects.all().order_by('-created_at')
    bform = Batch()
    if request.method == 'POST':
        data = request.POST
        #print(data)
        bform.name = data["b_name"]
        bform.project = Project.objects.get(name=data["p_name"])
        bform.location = data["location"]
        bform.short_description = data["sdec"]
        bform.description = data["dec"]
        bform.created_by = request.user

        path = os.path.join('static/data', str(request.user.id), data["b_name"])
        try:
            os.makedirs(path)
        except Exception as e:
            pass

        zip_path = path + "/" + request.FILES['batch_fn'].name
        extracted_path = path + "/extracted/"

        with open(zip_path, 'wb') as f:
            f.write(request.FILES['batch_fn'].read())

        try:
            os.makedirs(path + '/extracted/')
        except:
            pass

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(path + "/extracted/")
        im_files = []

        for root, dirs, files in os.walk(extracted_path):
            for f in files:
                if f.endswith('.jpeg') or f.endswith('.JPG') or f.endswith('.jpg') or f.endswith('.png'):
                    im_files.append(os.path.join(root, f))
        print(files, len(files))
        bform.total_images = len(im_files)
        bform.save()
        for file in files:
            bank = ImageBank()
            # print(request.scheme,'://',request.META.HTTP_HOST)
            bank.URL = extracted_path + "/" + file
            bank.file_name = file
            bank.batch = bform
            bank.save()
        return redirect('batch')

    return render(request, 'batch/cbatch.html', {'projects': projects})


@login_required(login_url='index')
def createPjt(request):
    '''returns the batch page templet'''
    pform = Project()
    if request.method == 'POST':
        data = request.POST

        pform.name = data["p_name"]
        pform.locations = data["locations"]
        pform.sample_type = data["sample"]
        pform.short_description = data["sdec"]
        pform.description = data["dec"]
        pform.pcreated_by = request.user
        # print(data, request.user.username)
        # print(pform.pcreated_by)
        # if pform.is_valid():'Project' object has no attribute 'is_valid'
        pform.save()
        return redirect('project')

    return render(request, 'batch/cproject.html')

@login_required(login_url='index')
def get_project_location(request):
    project_id = request.GET.get('projectID')
    loc_s = Project.objects.get(name=project_id).locations
    loc_s = loc_s.split(',')
    return render(request, 'batch/selectLoc.html', {'loc_s': loc_s})

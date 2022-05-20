from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError



import random
from datetime import datetime, timezone

from . import models
from . import forms

# Create your views here.
def index(request):
    if request.method == "POST":
        form = forms.GalleryForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            form = forms.GalleryForm()
    else:
        form = forms.GalleryForm()

    gallery_objects = models.GalleryModel.objects.all().order_by("-published_on")
    gallery_list = []
    for gall in gallery_objects:
        temp_gall = {}
        temp_gall["gallery"] = gall.gallery
        temp_gall["id"] = gall.id
        temp_gall["author"] = gall.author.username
        temp_gall["date"] = gall.published_on.strftime("%Y-%m-%d")
        if gall.image:
             temp_gall["image"] = gall.image.url
             temp_gall["image_desc"] = gall.image_description
        else:
             temp_gall["image"] = ""
             temp_gall["image_desc"] = ""
        gallery_list += [temp_gall]

    context = {
        "title": "W.I. Construction",
        "body":"Hello World",
        "form": form,
        "gallery_list":gallery_list,
    }
    return render(request,"index.html", context=context)


def gallery_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        form = forms.GalleryForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            return redirect("/")
    else:
        form = forms.GalleryForm()

    context = {
        "title": "Add Post",
       "form": form,
    }
    return render(request,"gallery2.html", context=context)

def delete_random(request):
    some_list = models.GalleryModel.objects.all()
    some_int = random.randrange(len(some_list))
    some_instance = some_list[some_int]
    some_instance.delete()
    print(some_int)
    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/login/")

def register_view(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect("/login/")
    else:
        form = forms.RegistrationForm()

    context = {
        "title": "Registration Page",
         "form": form
    }
    return render(request,"registration/register.html", context=context)

def galls_view(request):
    gallery_objects = models.GalleryModel.objects.all().order_by("-published_on")
    gallery_list = {}
    gallery_list["galls"] = []
    for gall in gallery_objects:
        comment_objects = models.CommentModel.objects.filter(
            gallery=gall
            )
        temp_gall = {}
        temp_gall["gallery"] = gall.gallery
        temp_gall["id"] = gall.id
        temp_gall["author"] = gall.author.username
        temp_gall["date"] = gall.published_on.strftime("%Y-%m-%d")
        if gall.image:
            temp_gall["image"] = gall.image.url
            temp_gall["image_desc"] = gall.image_description
        else:
            temp_gall["image"] = ""
            temp_gall["image_desc"] = ""        
        gallery_list["galls"] += [temp_gall]

    return JsonResponse(gallery_list)

def about_view(request):
    context = {
        "title": "About Page",
    }
    return render(request, "about.html", context=context)

def service_view(request):
    context = {
        "title": "Service Page",
    }
    return render(request, "service.html", context=context)


def contact_view(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #assert False
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'contact.html', {'form': form, 'submitted': submitted})
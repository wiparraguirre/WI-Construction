from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


import random
from datetime import datetime, timezone

from . import models
from . import forms

# Create your views here.
def index(request):
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            form = forms.SuggestionForm()
    else:
        form = forms.SuggestionForm()

    context = {
        "title": "WI Constrcution",
       "form": form
    }
    return render(request,"index.html", context=context)

@login_required
def comment_view(request, sugg_id):
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, sugg_id)
            return redirect("/")
    else:
        form = forms.CommentForm()

    context = {
        "title": "Comment",
        "sugg_id": sugg_id,
       "form": form
    }
    return render(request,"comment.html", context=context)

def suggestion_view(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            return redirect("/")
    else:
        form = forms.SuggestionForm()

    context = {
        "title": "Add Image",
       "form": form
    }
    return render(request,"suggestion.html", context=context)

def delete_random(request):
    some_list = models.SuggestionModel.objects.all()
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

def suggestions_view(request):
    suggestion_objects = models.SuggestionModel.objects.all()
    suggestion_list = {}
    suggestion_list["suggestions"] = []
    for sugg in suggestion_objects:
        comment_objects = models.CommentModel.objects.filter(
            suggestion=sugg
            )
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        temp_sugg["id"] = sugg.id
        temp_sugg["author"] = sugg.author.username
        temp_sugg["date"] = sugg.published_on.strftime("%Y-%m-%d")
        temp_sugg["comments"] = []
        for comm in comment_objects:
            temp_comm = {}
            temp_comm["comment"] = comm.comment
            temp_comm["id"] = comm.id
            temp_comm["author"] = comm.author.username
            time_diff = datetime.now(timezone.utc) - comm.published_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_comm["date"] = "published " + str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s,60)[0]
                if time_diff_m < 60:
                    temp_comm["date"] = "published " + str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m,60)[0]
                    if time_diff_h < 24:
                        temp_comm["date"] = "published " + str(int(time_diff_h)) + " hours ago"
                    else:
                        temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S")
            temp_sugg["comments"] += [temp_comm]
        suggestion_list["suggestions"] += [temp_sugg]

    return JsonResponse(suggestion_list)
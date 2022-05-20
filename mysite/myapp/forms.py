from django import forms
from django.contrib import auth
from django.core import validators
from django.core.validators import validate_unicode_slug
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user

from . import models

def must_be_unique(value):
    user_objects = auth_user.objects.filter(email=value)
    if len(user_objects) > 0:
        raise forms.ValidationError("Email already exists")
    # Always return the cleaned data
    return value


class GalleryForm(forms.Form):
    gallery_field = forms.CharField(
        label='Post',
        max_length=240,
        )
    image = forms.ImageField(
        label="Image File",
        required=False,
    )
    image_description = forms.CharField(
        label="Image Description",
        max_length=240,
        required=False
    )

    def save(self, request):
        gallery_instance = models.GalleryModel()
        gallery_instance.gallery = self.cleaned_data["gallery_field"]
        #gallery_instance.image = self.cleaned_data["image"]
        gallery_instance.image_description = self.cleaned_data["image_description"]
        gallery_instance.author = request.user
        gallery_instance.save()
        return gallery_instance

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )

    class Meta:
        model = auth_user
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    firstname = forms.CharField(max_length = 100, required = True, label="Your first name")
    lastname = forms.CharField(max_length = 100, required = True, label="Your last name")
    email = forms.CharField(max_length = 150, required = True, label="Email Address")
    message = forms.CharField(widget = forms.Textarea, max_length = 2000, required = True)


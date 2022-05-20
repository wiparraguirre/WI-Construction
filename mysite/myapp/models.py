from django.db import models
from django.contrib.auth.models import User as auth_user
from PIL import Image

# Create your models here.
class GalleryModel(models.Model):
    gallery = models.CharField(max_length=240)
    author = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to = 'uploads/%Y/%m/%d/',
        null=True
    )
    image_description = models.CharField(
        max_length=240,
        null=True
    )

    def __str__(self):
        return str(self.author.username) + " " + str(self.gallery)


#class Contact(models.Model):
 #   email = models.EmailField()
  #  subject = models.CharField(max_length=255)
   # message = models.TextField()

    #def __str__(self):
     #   return self.email
# Generated by Django 3.2.7 on 2022-05-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_remove_gallerymodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallerymodel',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
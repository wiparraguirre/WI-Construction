# Generated by Django 3.2.7 on 2022-03-13 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20211026_0106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestionmodel',
            name='author',
        ),
        migrations.DeleteModel(
            name='CommentModel',
        ),
        migrations.DeleteModel(
            name='SuggestionModel',
        ),
    ]

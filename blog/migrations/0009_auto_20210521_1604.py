# Generated by Django 3.2.3 on 2021-05-21 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_landingpage_social_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='avatar',
            field=models.ImageField(upload_to='blog/static/uploads/LandingPageStuff'),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='resume',
            field=models.FileField(upload_to='blog/static/uploads/LandingPageStuff'),
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210521_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='avatar',
            field=models.ImageField(upload_to='uploads/LandingPageStuff'),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='resume',
            field=models.FileField(upload_to='uploads/LandingPageStuff'),
        ),
    ]
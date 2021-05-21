# Generated by Django 3.2.3 on 2021-05-21 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210521_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='index/images'),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='resume',
            field=models.FileField(upload_to='index/docs'),
        ),
        migrations.DeleteModel(
            name='SocialMedia',
        ),
    ]
# Generated by Django 3.2.3 on 2021-05-23 08:07

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_project_bg_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='bg_img',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=-1, size=[1000, 730], upload_to='project/images'),
        ),
    ]

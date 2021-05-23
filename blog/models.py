from datetime import datetime
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django_resized import ResizedImageField
from django.utils import timezone
from django.contrib.auth.models import User

# for creating a canonical url for our post
from django.urls import reverse

# a model manager to get all published posts
class PublishedObjManager(models.Manager):
    def get_queryset(self):
        return (
            super(PublishedObjManager, self).get_queryset().filter(status="published")
        )


class Post(models.Model):
    objects = models.Manager()  # default manager
    published = PublishedObjManager()  # custome object manager
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date="publish"
    )  # this publish is connected to publish field
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    # canonical url
    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class career_post(models.Model):
    from_year = models.DateField()
    to_year = models.DateField(default=datetime.now)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    summary = models.TextField()

    def __str__(self):
        return self.company_name


class LandingPage(models.Model):
    avatar = models.ImageField(upload_to="index/images", null=True, blank=True)
    quote = models.TextField()
    intro = models.TextField()
    resume = models.FileField(upload_to="index/docs")
    social_json = models.JSONField(null=True)
    skills = models.TextField(max_length=400)


class Project(models.Model):
    bg_img = ResizedImageField(
        size=[1000, 730],
        quality=-1,
        upload_to="project/images",
        crop=["middle", "center"],
        force_format="PNG",
    )
    name = models.CharField(max_length=200)
    summary = models.TextField()
    features = models.TextField()
    tech_used = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "{self.name} : '{self.body}'"

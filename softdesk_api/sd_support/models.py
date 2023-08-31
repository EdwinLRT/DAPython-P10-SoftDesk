import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.conf import settings

CustomUser = get_user_model()


class Project(models.Model):
    """Project model"""
    TYPE_CHOICES = [
        ('Front-end', 'Front-end'),
        ('Back-end', 'Back-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)  # Champ de slug
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_projects')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Issue(models.Model):
    """Issue model"""
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_issues')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comments = models.ManyToManyField('self', symmetrical=False, related_name='related_issue_comments')

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Comment model"""
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='related_comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_comments')

    def __str__(self):
        return self.content


class Contributor(models.Model):
    """Contributor model"""
    PERMISSION_CHOICES = [
        ("Creator", "Creator"),
        ("Contributor", "Contributor"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='Contributor')

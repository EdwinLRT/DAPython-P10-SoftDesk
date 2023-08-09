import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

CustomUser = get_user_model()

from django.utils.text import slugify

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
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, default='temp')  # Champ de slug
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author', default=1)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)  # Génère un slug basé sur le titre
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Le reste de vos modèles reste inchangé.

class Comment(models.Model):
    """Comment model"""
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Contributor(models.Model):
    """Contributor model"""
    project = models.ManyToManyField('Project', related_name='contributors')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
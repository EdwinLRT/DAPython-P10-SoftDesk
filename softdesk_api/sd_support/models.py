from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """User model"""
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    identifiants = models.CharField(max_length=100, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Project(models.Model):
    """Project model"""
    TYPE_CHOICES = [
        ('Front-end', 'Front-end'),
        ('Back-end', 'Back-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class Issue(models.Model):
    """Issue model"""
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
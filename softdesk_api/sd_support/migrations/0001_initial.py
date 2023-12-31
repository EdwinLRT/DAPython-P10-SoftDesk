# Generated by Django 4.2.4 on 2023-08-24 15:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('Front-end', 'Front-end'), ('Back-end', 'Back-end'), ('iOS', 'iOS'), ('Android', 'Android')], max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('priority', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_issues', to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(related_name='related_issue_comments', to='sd_support.issue')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sd_support.project')),
            ],
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_author', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sd_support.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_comments', to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_comments', to='sd_support.issue')),
            ],
        ),
    ]

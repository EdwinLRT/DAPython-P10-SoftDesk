# Generated by Django 4.2.4 on 2023-08-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sd_support', '0002_rename_owner_project_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contributor',
            name='is_author',
        ),
        migrations.AddField(
            model_name='contributor',
            name='permission',
            field=models.CharField(choices=[('Creator', 'Creator'), ('Contributor', 'Contributor')], default='Contributor', max_length=20),
        ),
    ]

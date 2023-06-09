# Generated by Django 4.2.1 on 2023-05-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_userprofile_avatar_url_userprofile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

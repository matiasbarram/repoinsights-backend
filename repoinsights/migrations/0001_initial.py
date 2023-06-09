# Generated by Django 4.2.1 on 2023-05-16 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField()),
                ('ext_ref_id', models.CharField(max_length=32)),
                ('type', models.CharField(default='USR', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField()),
                ('ext_ref_id', models.CharField(max_length=32)),
                ('forked_from', models.IntegerField(null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='repoinsights.user')),
            ],
            options={
                'db_table': 'projects',
            },
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-16 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metabase', '0002_rename_metabse_id_metabaseuserdata_metabase_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='metabaseuserdata',
            name='metabase_group_id',
            field=models.IntegerField(default=-1),
        ),
    ]

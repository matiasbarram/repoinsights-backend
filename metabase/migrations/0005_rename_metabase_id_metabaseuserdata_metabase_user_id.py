# Generated by Django 4.2.1 on 2023-06-01 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metabase', '0004_metabaseuserdata_metabase_db_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metabaseuserdata',
            old_name='metabase_id',
            new_name='metabase_user_id',
        ),
    ]

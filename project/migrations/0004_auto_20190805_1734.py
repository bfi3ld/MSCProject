# Generated by Django 2.2.3 on 2019-08-05 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_submission_is_original'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission_edits',
            old_name='original_submission',
            new_name='submission',
        ),
    ]

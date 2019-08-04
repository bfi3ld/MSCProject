# Generated by Django 2.2.3 on 2019-08-04 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission_edits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delta', models.TextField()),
                ('date_time', models.DateTimeField()),
                ('original_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Submission')),
            ],
        ),
    ]
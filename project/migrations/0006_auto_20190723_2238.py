# Generated by Django 2.2.3 on 2019-07-23 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20190723_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patch',
            name='number',
        ),
        migrations.AddField(
            model_name='patch',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]

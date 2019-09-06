# Generated by Django 2.2.1 on 2019-09-01 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20190827_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgement',
            name='patch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Patch'),
        ),
        migrations.AlterField(
            model_name='peer_review_rubrik',
            name='patch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Patch'),
        ),
        migrations.AlterField(
            model_name='round',
            name='patch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Patch'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='patch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Patch'),
        ),
    ]
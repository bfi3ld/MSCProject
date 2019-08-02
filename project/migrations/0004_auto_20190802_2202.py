# Generated by Django 2.2.3 on 2019-08-02 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20190801_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peer_review_submission',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Student'),
        ),
        migrations.AlterField(
            model_name='peer_review_submission',
            name='peer_review_rubrik',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Peer_review_rubrik'),
        ),
    ]
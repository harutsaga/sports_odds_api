# Generated by Django 3.2.12 on 2022-02-05 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='e_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# Generated by Django 3.2.12 on 2022-02-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_market_market_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='self_market_id',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 3.2.12 on 2022-02-11 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20220208_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='awayName',
            field=models.CharField(blank=True, db_index=True, help_text='Away team name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='homeName',
            field=models.CharField(blank=True, db_index=True, help_text='Home team name', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='league',
            field=models.CharField(choices=[('NBA', 'NBA'), ('MLB', 'MLB'), ('NHL', 'NHL'), ('NFL', 'NFL')], db_index=True, default='NBA', help_text='League', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(db_index=True, help_text='Name of the event. e.g., Metropolitan Division @ Atlantic Division', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='sports',
            field=models.CharField(choices=[('Basketball', 'Basketball'), ('Baseball', 'Baseball'), ('Ice Hockey', 'Ice Hockey'), ('Football', 'Football')], db_index=True, default='Basketball', help_text='Sport Type', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='startTime',
            field=models.DateTimeField(blank=True, db_index=True, help_text='Start time of the event', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='updateTime',
            field=models.DateTimeField(blank=True, help_text='Updated time', null=True),
        ),
    ]

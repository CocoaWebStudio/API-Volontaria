# Generated by Django 2.1.5 on 2019-05-27 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiVolontaria', '10001_auto_20180430_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='volunteer_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 2.2.12 on 2022-07-05 06:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0005_auto_20220704_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
    ]

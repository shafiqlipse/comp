# Generated by Django 5.0.6 on 2024-07-25 06:55

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_quill.fields.QuillField(),
        ),
    ]

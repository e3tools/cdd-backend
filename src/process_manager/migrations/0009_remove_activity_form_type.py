# Generated by Django 4.0.4 on 2023-08-04 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('process_manager', '0008_formtype_formfield_activity_form_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='form_type',
        ),
    ]
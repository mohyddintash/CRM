# Generated by Django 3.1.7 on 2021-03-06 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_auto_20210305_2125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='user_profile',
            new_name='oraganisation',
        ),
    ]

# Generated by Django 2.2.4 on 2019-09-04 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_partner_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='contract',
            new_name='contact',
        ),
    ]

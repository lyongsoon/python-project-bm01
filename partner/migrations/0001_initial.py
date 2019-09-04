# Generated by Django 2.2.4 on 2019-09-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('contract', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
    ]
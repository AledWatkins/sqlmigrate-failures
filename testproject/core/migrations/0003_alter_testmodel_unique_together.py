# Generated by Django 4.0.4 on 2022-05-23 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_testmodel_colour'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='testmodel',
            unique_together={('name', 'colour')},
        ),
    ]

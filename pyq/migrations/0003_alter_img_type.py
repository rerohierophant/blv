# Generated by Django 3.2.24 on 2024-02-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyq', '0002_userprofile_emotional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='type',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]

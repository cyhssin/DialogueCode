# Generated by Django 4.1.13 on 2024-12-09 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
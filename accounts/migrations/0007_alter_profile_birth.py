# Generated by Django 4.1.13 on 2024-12-10 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
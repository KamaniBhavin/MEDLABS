# Generated by Django 2.2.7 on 2019-11-04 10:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0007_auto_20191102_0506'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='encrypted_storage',
            new_name='file_storage',
        ),
    ]
# Generated by Django 2.2.4 on 2020-03-12 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_authenticator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='pw',
            new_name='password',
        ),
    ]

# Generated by Django 2.2.4 on 2020-03-10 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200209_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='pw',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]

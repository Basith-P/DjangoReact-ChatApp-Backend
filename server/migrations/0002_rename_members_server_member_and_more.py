# Generated by Django 4.2.4 on 2023-09-05 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='members',
            new_name='member',
        ),
        migrations.AlterField(
            model_name='server',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]

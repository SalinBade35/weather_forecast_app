# Generated by Django 5.1.1 on 2024-10-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudApp1', '0010_alter_studentleave_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentleave',
            name='document',
            field=models.FileField(null=True, upload_to='documents/'),
        ),
    ]

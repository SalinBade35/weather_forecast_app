# Generated by Django 5.1.1 on 2024-10-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudApp1', '0005_rename_delete_data_studentleave_deleted_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentleave',
            name='student_email',
            field=models.EmailField(default='no-email@example.com', max_length=100),
            preserve_default=False,
        ),
    ]

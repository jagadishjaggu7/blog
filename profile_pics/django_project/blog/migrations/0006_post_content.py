# Generated by Django 4.2.7 on 2023-11-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default='heyy', max_length=500),
        ),
    ]

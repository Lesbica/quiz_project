# Generated by Django 5.1.3 on 2024-12-04 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]

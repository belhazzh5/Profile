# Generated by Django 3.0.8 on 2022-08-02 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20220802_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateField(),
        ),
    ]
# Generated by Django 3.2.7 on 2021-09-20 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createuser',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-28 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210928_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createuser',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
    ]
# Generated by Django 4.2.3 on 2023-07-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_alter_test_options_laboratory_google_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratory',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='laboratory',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
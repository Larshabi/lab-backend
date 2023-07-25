# Generated by Django 4.2.3 on 2023-07-25 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0003_alter_laboratory_latitude_alter_laboratory_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='laboratory',
        ),
        migrations.RemoveField(
            model_name='test',
            name='price',
        ),
        migrations.CreateModel(
            name='TestPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('laboratory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.laboratory')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.test')),
            ],
            options={
                'verbose_name': 'Test Prices',
            },
        ),
    ]
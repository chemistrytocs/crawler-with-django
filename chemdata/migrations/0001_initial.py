# Generated by Django 2.0.2 on 2018-09-06 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('maker', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('pury', models.CharField(max_length=50)),
                ('cas', models.CharField(max_length=50)),
                ('pack', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('stock', models.CharField(max_length=50)),
            ],
        ),
    ]

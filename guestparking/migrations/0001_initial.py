# Generated by Django 3.0.3 on 2020-02-24 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('hash', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate', models.TextField()),
                ('starttime', models.DateTimeField()),
                ('parked', models.BooleanField(default=True)),
                ('endtime', models.DateTimeField(null=True)),
                ('blocked', models.BooleanField(default=False)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guestparking.Flat')),
            ],
        ),
    ]

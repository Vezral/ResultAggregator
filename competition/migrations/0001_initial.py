# Generated by Django 2.0.4 on 2018-05-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
    ]

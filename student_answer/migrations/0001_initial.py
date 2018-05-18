# Generated by Django 2.0.4 on 2018-05-07 12:48

from django.db import migrations, models
import django.db.models.deletion
import student_answer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_time', models.DateTimeField(auto_now_add=True)),
                ('answer_file', models.FileField(upload_to=student_answer.models.upload_directory)),
                ('correct_count', models.IntegerField(null=True)),
                ('solved', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswerResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_file', models.FileField(upload_to=student_answer.models.upload_directory)),
                ('is_correct', models.BooleanField(default=False)),
                ('student_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_answer.StudentAnswer')),
            ],
        ),
    ]

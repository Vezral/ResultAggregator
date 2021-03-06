from django.db import models
from django.contrib.auth.models import User
from competition.models import Competition
from question.models import Question
from user.models import Student
import os


# determine the upload_directory for uploaded student_answer file (including answer) in MEDIA_ROOT
def upload_directory(instance, filename):
    path = os.path.join(str(instance.question.competition.id), str(instance.question.id))
    path = os.path.join(path, filename)
    return path


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)
    answer_file = models.FileField(upload_to=upload_directory)
    correct_count = models.IntegerField(null=True)
    solved = models.BooleanField(default=False)

    def get_answer_file_text(self):
        file = open(self.answer_file.path, 'r')
        return file.read()

    def __str__(self):
        return '{} {} {} {}'.format(str(self.pk), self.student.user.username, self.answer_file.path, self.submission_time)


class StudentAnswerResult(models.Model):
    student_answer = models.ForeignKey(StudentAnswer, on_delete=models.CASCADE)
    result_file = models.FileField(upload_to=upload_directory)
    is_correct = models.BooleanField(default=False)

    def get_result_file_text(self):
        file = open(self.result_file.path, 'r')
        return file.read()

    def __str__(self):
        return '{} {}'.format(self.result_file.path, str(self.is_correct))

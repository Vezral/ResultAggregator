from django.db import models
from django.urls import reverse
from competition.models import Competition
import os


# determine the upload_directory for uploaded question file (including answer) in MEDIA_ROOT
def upload_directory(instance, filename):
    path = os.path.join(str(instance.question.competition.id), str(instance.question.id))
    path = os.path.join(path, filename)
    return path


class Question(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('question:question-details', kwargs={'question_pk': self.pk})

    def __str__(self):
        return '{} {} {}'.format(str(self.pk), self.name, self.creation_date)


class QuestionFile(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_file = models.FileField(upload_to=upload_directory)
    answer_file = models.FileField(upload_to=upload_directory)

    def get_question_file_text(self):
        file = open(self.question_file.path, 'r')
        return file.read()

    def get_answer_file_text(self):
        file = open(self.answer_file.path, 'r')
        return file.read()

    def __str__(self):
        return '{} || {}'.format(self.question_file.name, self.answer_file.name)

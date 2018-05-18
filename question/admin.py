from django.contrib import admin
from .models import Question, QuestionFile

admin.site.register(Question)
admin.site.register(QuestionFile)

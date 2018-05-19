from django.views.generic import RedirectView
from django.urls import path, include, re_path
from question.views import *

app_name = 'question'

urlpatterns = [
    # /competition/<competition_pk>/question/
    path('<int:question_pk>/', DetailsView.as_view(), name='question-details'),
    path('add/', QuestionCreate.as_view(), name='question-add'),
    path('<int:question_pk>/delete/', QuestionDelete.as_view(), name='question-delete'),
    path('<int:question_pk>/update/', QuestionUpdate.as_view(), name='question-update'),
    path('<int:question_pk>/question_file/add/', QuestionFileCreate.as_view(), name='question-file-add'),
    path('<int:question_pk>/question_file/<int:question_file_pk>/delete/', QuestionFileDelete.as_view(), name='question-file-delete'),
    path('<int:question_pk>/question_file/<int:question_file_pk>/update/', QuestionFileUpdate.as_view(), name='question-file-update'),
    path('<int:question_pk>/student_answer/', include('student_answer.urls')),
    re_path(r'^.*$', RedirectView.as_view(url='/')),
]

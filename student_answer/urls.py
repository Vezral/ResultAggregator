from django.urls import path, re_path
from student_answer import views
from django.views.generic import RedirectView

app_name = 'student_answer'

urlpatterns = [
    # /competition/<competition_pk>/question/<question_pk>/student_answer/
    path('add/', views.StudentAnswerCreate.as_view(), name='student-answer-add'),
    path('<int:student_answer_pk>/delete/', views.StudentAnswerDelete.as_view(), name='student-answer-delete'),
    path('<int:student_answer_pk>/update/', views.StudentAnswerUpdate.as_view(), name='student-answer-update'),
    re_path(r'^.*$', RedirectView.as_view(url='/')),
]

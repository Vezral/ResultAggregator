from django.views.generic import RedirectView
from django.urls import path, include, re_path
from competition.views import *

app_name = 'competition'

urlpatterns = [
    # /competition
    path('', IndexView.as_view(), name='competition-index'),
    path('<int:competition_pk>/', DetailsView.as_view(), name='competition-details'),
    path('add/', CompetitionCreate.as_view(), name='competition-add'),
    path('<int:competition_pk>/delete/', CompetitionDelete.as_view(), name='competition-delete'),
    path('<int:competition_pk>/update/', CompetitionUpdate.as_view(), name='competition-update'),
    path('<int:competition_pk>/change_archive/', change_competition_archive_status, name='competition-change-archive-status'),
    path('<int:competition_pk>/start_competition/', start_competition, name='competition-start'),
    path('<int:competition_pk>/restart_competition/', restart_competition, name='competition-restart'),
    path('<int:competition_pk>/stop_competition/', stop_competition, name='competition-stop'),
    path('<int:competition_pk>/join_competition/', join_competition, name='competition-join'),
    path('<int:competition_pk>/remove_student/', remove_student_from_competition, name='competition-remove-student'),
    path('<int:competition_pk>/competition_result/', GenerateResultTable.as_view(), name='competition-generate-result'),
    path('<int:competition_pk>/competition_result_ajax/', generate_result_table_ajax, name='competition-generate-result-ajax'),
    path('<int:competition_pk>/question/', include('question.urls')),
    re_path(r'^.*$', RedirectView.as_view(url='/')),
]

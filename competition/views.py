from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from .models import Competition
from helper_functions.generate_competition_table import generate_competition_table
from datetime import datetime
from user.models import Student


class IndexView(ListView):
    template_name = 'competition/index.html'
    context_object_name = 'competition_list'

    def get_queryset(self):
        return Competition.objects.all()


class DetailsView(ListView):
    template_name = 'competition/details.html'
    context_object_name = 'competition'

    def get_queryset(self):
        return Competition.objects.get(pk=self.kwargs['competition_pk'])


class GenerateResultTable(TemplateView):
    pk_url_kwargs = 'competition_pk'
    template_name = 'competition/result_table.html'

    def get_context_data(self, **kwargs):
        context = super(GenerateResultTable, self).get_context_data(**kwargs)
        context['competition_pk'] = self.kwargs['competition_pk']
        context['table'] = generate_competition_table(self.kwargs['competition_pk'])
        return context


class CompetitionCreate(CreateView):
    model = Competition
    fields = ['name']
    template_name = 'competition/competition_form.html'

    def get_success_url(self):
        competition_pk = self.object.id
        return reverse('competition:competition-details', kwargs={'competition_pk': competition_pk})


class CompetitionUpdate(UpdateView):
    model = Competition
    fields = ['name']
    template_name = 'competition/competition_form.html'
    pk_url_kwarg = 'competition_pk'
    success_url = reverse_lazy('competition:competition-index')


class CompetitionDelete(DeleteView):
    model = Competition
    pk_url_kwarg = 'competition_pk'
    success_url = reverse_lazy('competition:competition-index')


def change_competition_archive_status(request, **kwargs):
    competition = Competition.objects.get(pk=kwargs['competition_pk'])
    competition.is_archived = 1 - competition.is_archived
    competition.save()
    return redirect('competition:competition-index')


def start_competition(request, **kwargs):
    competition = Competition.objects.get(pk=kwargs['competition_pk'])
    competition.start_time = datetime.now()
    competition.is_active = True
    competition.save()
    return redirect('competition:competition-details', competition_pk=competition.id)


def restart_competition(request, **kwargs):
    competition = Competition.objects.get(pk=kwargs['competition_pk'])
    # set user as inactive and log them out
    for student in competition.student_set.all():
        for student_answer in student.studentanswer_set.filter(question__competition=competition):
            student_answer.delete()
        student.competition.remove(competition)
    competition.start_time = datetime.now()
    competition.save()
    return redirect('competition:competition-details', competition_pk=competition.id)


def stop_competition(request, **kwargs):
    competition = Competition.objects.get(pk=kwargs['competition_pk'])
    competition.is_active = False
    competition.save()
    return redirect('competition:competition-details', competition_pk=competition.id)


def join_competition(request, **kwargs):
    student = Student.objects.get(user=request.user)
    competition = Competition.objects.get(pk=kwargs['competition_pk'])
    student.competition.add(competition)
    return redirect('competition:competition-details', competition_pk=competition.id)


def remove_student_from_competition(request, **kwargs):
    if request.method == 'POST':
        student = Student.objects.get(pk=request.POST['student_id'])
        competition = Competition.objects.get(pk=kwargs['competition_pk'])
        student.competition.remove(competition)
        return redirect('competition:competition-generate-result', competition_pk=competition.id)


def generate_result_table_ajax(request, **kwargs):
    table = generate_competition_table(kwargs['competition_pk'])
    return render(request, 'competition/result_table_ajax.html', {'table': table})

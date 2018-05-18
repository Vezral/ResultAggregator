from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse
from helper_functions.file_management import trim_text_file
from .models import Question, QuestionFile
from student_answer.models import StudentAnswer
from user.models import Student
from competition.models import Competition


class DetailsView(DetailView):
    model = Question
    template_name = 'question/details.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)
        # if question solved, remove 'Add Question' button and add red Solved header
        if self.request.user.groups.filter(name='Student').exists():
            student = Student.objects.get(user=self.request.user)
            context['solved'] = False
            student_answer = StudentAnswer.objects.filter(student=student, question=self.kwargs['question_pk'])
            context['student_answer_list'] = student_answer
            if student_answer.filter(solved=True).count() > 0:
                context['solved'] = True
        elif self.request.user.groups.filter(name='Lecturer').exists():
            context['student_answer_list'] = StudentAnswer.objects.filter(
                question=self.kwargs['question_pk'],
                student__user__is_active=True,
            )
        return context


class QuestionCreate(CreateView):
    model = Question
    fields = ['name', 'description']
    template_name = 'question/question_form.html'

    def form_valid(self, form):
        competition_pk = self.kwargs.get('competition_pk')
        form.instance.competition = Competition.objects.get(pk=competition_pk)
        form.save()
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.object.id
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk
        })


class QuestionUpdate(UpdateView):
    model = Question
    pk_url_kwarg = 'question_pk'
    fields = ['name', 'description']
    template_name = 'question/question_form.html'

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        return reverse('competition:competition-details', kwargs={'competition_pk': competition_pk})


class QuestionDelete(DeleteView):
    model = Question
    pk_url_kwarg = 'question_pk'

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        return reverse('competition:competition-details', kwargs={'competition_pk': competition_pk})


class QuestionFileCreate(CreateView):
    model = QuestionFile
    pk_url_kwarg = 'question_pk'
    fields = ['question_file', 'answer_file']
    template_name = 'question/question_file_form.html'

    def form_valid(self, form):
        question_pk = self.kwargs.get('question_pk')
        form.instance.question = Question.objects.get(pk=question_pk)
        form.save()
        question_file = QuestionFile.objects.get(pk=form.instance.id)
        trim_text_file(question_file.question_file.path)
        trim_text_file(question_file.answer_file.path)
        return super(QuestionFileCreate, self).form_valid(form)

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.kwargs.get('question_pk')
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk,
        })


class QuestionFileUpdate(UpdateView):
    model = QuestionFile
    fields = ['question_file', 'answer_file']
    template_name = 'question/question_file_form.html'
    pk_url_kwarg = 'question_file_pk'

    def form_valid(self, form):
        form.save()
        question_file = QuestionFile.objects.get(pk=form.instance.id)
        trim_text_file(question_file.question_file.path)
        trim_text_file(question_file.answer_file.path)
        return super(QuestionFileUpdate, self).form_valid(form)

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.kwargs.get('question_pk')
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk,
        })


class QuestionFileDelete(DeleteView):
    model = QuestionFile
    pk_url_kwarg = 'question_file_pk'

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.kwargs.get('question_pk')
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk,
        })

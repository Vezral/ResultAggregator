from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from question.models import Question
from .models import StudentAnswer, StudentAnswerResult
from user.models import Student
from helper_functions.run_java_file import run_java_program


class StudentAnswerCreate(CreateView):
    model = StudentAnswer
    fields = ['answer_file']
    pk_url_kwarg = 'question_pk'
    template_name = 'student_answer/student_answer_form.html'

    def form_valid(self, form):
        source_code_name = form.instance.answer_file.name
        form.instance.student = Student.objects.get(user=self.request.user)
        question_pk = self.kwargs.get('question_pk')
        form.instance.question = Question.objects.get(pk=question_pk)
        form.save()
        correct_count = run_java_program(form.instance.id, source_code_name)
        form.instance.correct_count = correct_count
        if correct_count == form.instance.question.questionfile_set.count():
            form.instance.solved = True
        return super(StudentAnswerCreate, self).form_valid(form)

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.kwargs.get('question_pk')
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk,
        })


class StudentAnswerUpdate(UpdateView):
    model = StudentAnswer
    fields = ['answer_file']
    template_name = 'student_answer/student_answer_form.html'
    pk_url_kwarg = 'student_answer_pk'

    def form_valid(self, form):
        source_code_name = form.instance.answer_file.name
        form.save()
        student_answer_pk = form.instance.id
        StudentAnswerResult.objects.filter(student_answer=student_answer_pk).delete()
        correct_count = run_java_program(student_answer_pk, source_code_name)
        form.instance.correct_count = correct_count
        return super(StudentAnswerUpdate, self).form_valid(form)

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.kwargs.get('question_pk')
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk,
        })


class StudentAnswerDelete(DeleteView):
    model = StudentAnswer
    pk_url_kwarg = 'student_answer_pk'

    def get_success_url(self):
        competition_pk = self.kwargs.get('competition_pk')
        question_pk = self.kwargs.get('question_pk')
        return reverse('competition:question:question-details', kwargs={
            'competition_pk': competition_pk,
            'question_pk': question_pk,
        })

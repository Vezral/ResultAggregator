from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from .models import Student


class LecturerList(ListView):
    template_name = 'user/lecturer_list.html'
    context_object_name = 'lecturer_list'

    def get_queryset(self):
        return User.objects.all().filter(groups__name='Lecturer', is_active=True).exclude(pk=1)


class LecturerRegister(CreateView):
    form_class = UserCreationForm
    template_name = 'user/lecturer_register.html'

    def get_success_url(self):
        try:
            group = Group.objects.get(name='Lecturer')
        except Group.DoesNotExist:
            new_group = Group.objects.create(name='Lecturer')
            new_group.save()
            group = new_group
        group.user_set.add(self.object)
        return reverse('lecturer-list')


def lecturer_delete(request, **kwargs):
    if request.method == 'POST':
        lecturer = User.objects.get(pk=kwargs['lecturer_pk'])
        lecturer.is_active = False
        lecturer.save()
        return redirect('lecturer-list')


class StudentRegister(CreateView):
    form_class = UserCreationForm
    template_name = 'user/student_register.html'

    def get_success_url(self):
        user = self.object
        Student.objects.create(user=user)
        try:
            group = Group.objects.get(name='Student')
        except Group.DoesNotExist:
            new_group = Group.objects.create(name='Student')
            new_group.save()
            group = new_group
        group.user_set.add(user)

        # login new student user
        login(self.request, user)
        return reverse('competition:competition-index')


def student_delete(request, **kwargs):
    if request.method == 'POST':
        student = Student.objects.get(pk=request.POST['student_id'])
        student.user.is_active = False
        student.competition.remove(student)
        student.save()
        return redirect('competition:competition-generate-result')

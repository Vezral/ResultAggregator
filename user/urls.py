from django.urls import include, path
from .views import *

app_name = 'user'

urlpatterns = [
    # user/
    path('lecturer/', include('django.contrib.auth.urls')),
    path('lecturer/list/', LecturerList.as_view(), name='lecturer-list'),
    path('lecturer/register/', LecturerRegister.as_view(), name='lecturer-register'),
    path('lecturer/<int:lecturer_pk>/delete/', lecturer_delete, name='lecturer-delete'),
    path('student/', include('django.contrib.auth.urls')),
    path('student/register/', StudentRegister.as_view(), name='student-register'),
]

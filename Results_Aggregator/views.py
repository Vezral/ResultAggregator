from django.views.generic import TemplateView
from django.shortcuts import redirect, render


# if user hasn't login, redirect to homepage
class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('competition:competition-index')
        else:
            return render(request, 'Results_Aggregator/homepage.html')

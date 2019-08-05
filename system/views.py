from Ads_Project.functions import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from system.models import User, Tabligh


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        tablighs = Tabligh.objects.order_by('-id')[:10]

        return render(request, 'panel/index/dashboard.html', {'tablighs': tablighs})

from Ads_Project.functions import LoginRequiredMixin
from django.shortcuts import render

from django.views import View

from system.models import User


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        return render(request, 'system/dashboard.html', {'user': user})

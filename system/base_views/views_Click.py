from django.views import View
from django.views.generic import FormView
import encodings.base64_codec

from Ads_Project.functions import LoginRequiredMixin


class ClickedOnTablighView(LoginRequiredMixin, View):

    def get(self, request):
        pass

from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
import datetime
from django.utils import timezone

class AllowActiveUserOnly(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user.last_activity=timezone.now()
            request.user.save()
        return None
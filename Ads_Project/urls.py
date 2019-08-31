"""Ads_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404


from Ads_Project.settings import ADMIN_PANEL_URL
from system.base_views.views_User import login_user

def check_login_admin(request):
    if request.path==ADMIN_PANEL_URL:
        request.session['canloginasadmin'] = True
        return redirect(reverse('login'))
    raise Http404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_user, name='login'),
    path('system/', include('system.urls')),
    path('account/', include('allauth.urls')),
    url(r'^.*$', check_login_admin)
    # path('test/',lambda r:redirect('http://127.0.0.1/system/dashboard/?token=fqwfjqwohfqwifhuqwifuw'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
<form action="https://perfectmoney.is/api/step1.asp" method="POST">
<input type="hidden" name="PAYEE_ACCOUNT" value="U19586537">
<input type="hidden" name="PAYEE_NAME" value="افزایش اعتبار">
<input type="hidden" name="PAYMENT_ID" value="64dq98w4dqw9d84">
<input type="hidden" name="PAYMENT_AMOUNT" value="0.01">
<input type="hidden" name="PAYMENT_UNITS" value="USD">
<input type="hidden" name="STATUS_URL" value="http://f16cf625.ngrok.io/c">
<input type="hidden" name="PAYMENT_URL" value="http://f16cf625.ngrok.io/s">
<input type="hidden" name="PAYMENT_URL_METHOD" value="GET">
<input type="hidden" name="NOPAYMENT_URL" value="http://f16cf625.ngrok.io/f">
<input type="hidden" name="NOPAYMENT_URL_METHOD" value="GET">
<input type="hidden" name="INTERFACE_LANGUAGE" value="fa_IR">
<input type="hidden" name="SUGGESTED_MEMO" value="ندارد">
<input type="hidden" name="test1" value="test1">
<input type="hidden" name="BAGGAGE_FIELDS" value="test1">
<input type="submit" name="PAYMENT_METHOD" value="Pay Now!">
</form>
'''
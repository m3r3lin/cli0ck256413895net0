from django.contrib import messages
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json

from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView

from system.forms import PelanCreateForm
from system.models import Payam
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from system.models import User
from django.core import serializers


from system.templatetags.app_filters import date_jalali



class MessageListview(LoginRequiredMixin,ListView):
    model = Payam
    template_name = 'system/message/messagebox.html'
    # form_class = PelanCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        list_girande=[]
        newlist=[]
        user_message1=Payam.objects.filter(ferestande=self.request.user).order_by('id')

        for i in user_message1:
            last_item=Payam.objects.filter(ferestande=self.request.user,girande=i.girande).distinct().last()
            list_girande.append(last_item.id)
        #delte item tekrari in list
        for i in list_girande:
            if i not in newlist:
                newlist.append(i)


        user_message=Payam.objects.filter(id__in=newlist)

        context['user_message']=user_message
        return context






class Message_show_view(LoginRequiredMixin,TemplateView):
    template_name = "system/message/widgets.html"
    model = Payam
    # form_class = PelanCreateForm

    def get_context_data(self, **kwargs):
        context = super(Message_show_view, self).get_context_data(**kwargs)
        payam = get_object_or_404(Payam, pk=self.kwargs['pk'])
        print("payam frestande",payam.ferestande)
        print("payam girande",payam.girande)
        # q = Payam.objects.filter(ferestande=self.request.user)
        all_message=Payam.objects.filter(ferestande=payam.ferestande,girande=payam.girande)
        count_message=all_message.count()
        send_message=Payam.objects.filter(ferestande=payam.ferestande,girande=payam.girande)
        get_message=Payam.objects.filter(ferestande=payam.girande,girande=payam.ferestande)
        all_message=all_message.union(send_message,get_message).order_by('id')
        # print("all_message",all_message)
        # print("q is",q)
        # context['q']=q

        context['all_messsge']=all_message
        context['count_message']=count_message
        return context

    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     payam = get_object_or_404(Payam, pk=self.kwargs['pk'])
    #     print("payam girande", payam.girande)
    #     all_message = Payam.objects.filter(ferestande=payam.ferestande, girande=payam.girande)
    #     count_message = all_message.count()
    #     send_message = Payam.objects.filter(ferestande=payam.ferestande, girande=payam.girande)
    #     get_message = Payam.objects.filter(ferestande=payam.girande, girande=payam.ferestande)
    #     all_message = all_message.union(send_message, get_message).order_by('id')
    #     # context['all_messsge'] = all_message
    #     # context['count_message'] = count_message
    #
    #     message=self.request.POST.get('message',None)
    #     print("messsage",message)
    #     payam=Payam(ferestande=payam.ferestande,girande=payam.girande,
    #                 onvan="chat",text=message,vazeyat=2)
    #     payam.save()
    #     return render(request, self.template_name,{'all_message':all_message,'count_message':count_message})


# class save_message(TemplateView):

@csrf_exempt
def save_message(request):
    list = []
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        print("data",data)
        if data == "":
            data = "data"
            return HttpResponse()
        else:
            ferestande=data['ferestande']
            girande=data['girande']
            message=data['message']
            # print("frestande",ferestande)
            payam=Payam(ferestande=User.objects.get(username=ferestande),girande=User.objects.get(username=girande),onvan='chat',text=message,vazeyat=2)
            payam.save()
            last_payam=Payam.objects.filter(ferestande=User.objects.get(username=ferestande),girande=User.objects.get(username=girande)).last()
            # print("last_payam",last_payam)
            last_pyam_messsage=last_payam.text
            # message = Hamsar.objects.filter(hamsar=Soldier.objects.get(id=data))
            # for i in last_payam:
            #     list.append(i)
            # data = serializers.serialize("json", last_payam)
            # return HttpResponse(data, content_type="application/json")
            return JsonResponse({"last_pyam_messsage":last_pyam_messsage}, safe=False)

            # return HttpResponse(last_payam)

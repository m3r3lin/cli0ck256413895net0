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
from django.utils.decorators import method_decorator

from system.forms import PelanCreateForm
from system.models import Payam
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from system.models import User
from system.forms import NewMessageCreateForm
from django.core import serializers
from django.db.models import Q
from system.functions import check_role_user


from system.templatetags.app_filters import date_jalali


# class NewMessageCreateView(LoginRequiredMixin,CreateView):
#     model = Payam
#     template_name = 'system/message/Create_new_message.html'
#     form_class = NewMessageCreateForm
#
#
#     def form_valid(self, form):
#         payam = form.save(commit=False)
#         print("post",self.request.POST)
#         payam.vazeyat=2
#         payam.ferestande=self.request.user
#         payam.onvan='chat'
#         # payam.girande=self.request.POST.get('')
#
#         # messages.success(self.request, 'پیام مورد موردنظر  با موفقیت ثبت شد')
#         return super(NewMessageCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('MessageList')
#


class MessageListmoshahedeview(LoginRequiredMixin,ListView):
    model = Payam
    template_name = 'system/Moshahedat/Moshahedatmessagebox.html'
    # form_class = PelanCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        list_girande=[]
        newlist=[]
        user_message1=Payam.objects.all()
        print("user_message1",user_message1)
        user_message=Payam.objects.filter(Q(ferestande=self.request.user) | Q(girande=self.request.user)).distinct().last()




        for i in user_message1:
            last_item=Payam.objects.filter(Q(ferestande=i.ferestande,girande=i.girande)|Q(ferestande=i.girande,girande=i.ferestande)).last()
            print("last_item",last_item)


            try:
                list_girande.append(last_item.id)
            except:
                pass
        print("list_girande",list_girande)

        for i in list_girande:
            if i not in newlist:
                newlist.append(i)
        print("newlist",newlist)


        user_message=Payam.objects.filter(id__in=newlist)

        context['user_message']=user_message
        return context

    @method_decorator(check_role_user('administrator'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)






class Message_show_moshahedeview(LoginRequiredMixin,TemplateView):
    template_name = "system/Moshahedat/widgetsmoshahede.html"
    model = Payam
    # form_class = PelanCreateForm

    def get_context_data(self, **kwargs):
        context = super(Message_show_moshahedeview, self).get_context_data(**kwargs)
        payam = get_object_or_404(Payam, pk=self.kwargs['pk'])
        girande= None
        if payam.ferestande.id == self.request.user.id:
            girande = payam.girande
        elif payam.girande.id==self.request.user.id:
            girande=payam.ferestande


        # q = Payam.objects.filter(ferestande=self.request.user)
        all_message=Payam.objects.filter(ferestande=payam.ferestande,girande=payam.girande)
        # ten_message_last=Payam.objects.filter(ferestande=payam.ferestande,girande=payam.girande)[:10][::-1]
        # for i in ten_message_last:
        #     i.vazeyat=int(0)
        #     i.save()
            # print("vaziat",p.vazeyat)

        send_message=Payam.objects.filter(ferestande=payam.ferestande,girande=payam.girande)
        get_message=Payam.objects.filter(ferestande=payam.girande,girande=payam.ferestande)
        all_message=all_message.union(send_message,get_message).order_by('id')
        count_message=all_message.count()
        context['all_messsge']=all_message
        context['count_message']=count_message
        context['girande']=girande
        context['ferestande']=payam.ferestande
        return context


from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import TemplateView
from Ads_Project.functions import LoginRequiredMixin
from system.functions import check_role_user
from system.models import Payam


class MessageListmoshahedeview(LoginRequiredMixin, ListView):
    model = Payam
    template_name = 'system/Moshahedat/Moshahedatmessagebox.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        list_girande = []
        newlist = []
        user_message1 = Payam.objects.all()
        print("user_message1", user_message1)
        user_message = Payam.objects.filter(
            Q(ferestande=self.request.user) | Q(girande=self.request.user)).distinct().last()

        for i in user_message1:
            last_item = Payam.objects.filter(
                Q(ferestande=i.ferestande, girande=i.girande) | Q(ferestande=i.girande, girande=i.ferestande)).last()
            print("last_item", last_item)

            try:
                list_girande.append(last_item.id)
            except:
                pass
        print("list_girande", list_girande)

        for i in list_girande:
            if i not in newlist:
                newlist.append(i)
        print("newlist", newlist)

        user_message = Payam.objects.filter(id__in=newlist)

        context['user_message'] = user_message
        return context

    @method_decorator(check_role_user('administrator'))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class Message_show_moshahedeview(LoginRequiredMixin, TemplateView):
    template_name = "system/Moshahedat/widgetsmoshahede.html"
    model = Payam

    # form_class = PelanCreateForm

    def get_context_data(self, **kwargs):
        context = super(Message_show_moshahedeview, self).get_context_data(**kwargs)
        payam = get_object_or_404(Payam, pk=self.kwargs['pk'])
        girande = None
        if payam.ferestande.id == self.request.user.id:
            girande = payam.girande
        elif payam.girande.id == self.request.user.id:
            girande = payam.ferestande

        all_message = Payam.objects.filter(ferestande=payam.ferestande, girande=payam.girande)

        send_message = Payam.objects.filter(ferestande=payam.ferestande, girande=payam.girande)
        get_message = Payam.objects.filter(ferestande=payam.girande, girande=payam.ferestande)
        all_message = all_message.union(send_message, get_message).order_by('id')
        count_message = all_message.count()
        context['all_messsge'] = all_message
        context['count_message'] = count_message
        context['girande'] = girande
        context['ferestande'] = payam.ferestande
        return context

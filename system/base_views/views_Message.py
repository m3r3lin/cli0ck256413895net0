from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
import json
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from system.models import Payam
from django.views.generic import TemplateView
from django.http import HttpResponse
from system.models import User
from system.forms import NewMessageCreateForm
from django.db.models import Q
from django.contrib import messages


class NewMessageCreateView(LoginRequiredMixin, CreateView):
    model = Payam
    template_name = 'system/message/Create_new_message.html'
    form_class = NewMessageCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_girande = []
        get_user = User.objects.get(username=self.request.user)
        try:
            node_father_id = self.request.user.code_moaref.id
            list_girande.append(node_father_id)
        except:
            pass
        node_children_id = User.objects.filter(code_moaref=self.request.user)
        for i in node_children_id:
            list_girande.append(i.id)

        girande_admin = User.objects.filter(Q(roles__name='administrator'))
        for i in girande_admin:
            list_girande.append(i.id)
        # print("list_girande",list_girande)
        girande = User.objects.filter(id__in=list_girande).exclude(username=self.request.user)
        context['girande'] = girande
        return context
        # return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        print("post", self.request.POST)
        girande_id = self.request.POST.get('girande', None)
        message = self.request.POST.get('text', None)
        if girande_id is None or girande_id == '':
            messages.error(self.request, _("Please Specify Receiver"))
            return super().post(request, *args, **kwargs)

        payam = Payam(ferestande=self.request.user, girande_id=girande_id,
                      onvan='چت', text=message, vazeyat=1)
        payam.save()

        messages.success(self.request, _("The message is successfully created"))

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('MessageList')

    def form_valid(self, form):
        payam = form.save(commit=False)
        return self.render_to_response(self.get_context_data(form=form))


class MessageListview(LoginRequiredMixin, ListView):
    model = Payam
    template_name = 'system/message/messagebox.html'

    # form_class = PelanCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        list_girande = []
        newlist = []
        user_message1 = Payam.objects.filter(Q(ferestande=self.request.user) | Q(girande=self.request.user))

        for i in user_message1:
            last_item = Payam.objects.filter(
                Q(ferestande=self.request.user, girande=i.girande) | Q(ferestande=i.ferestande,
                                                                       girande=self.request.user)).last()
            try:
                list_girande.append(last_item.id)
                break
            except:
                pass
        # delte item tekrari in list
        for i in list_girande:
            if i not in newlist:
                newlist.append(i)

        user_message = Payam.objects.filter(id__in=newlist)

        context['user_message'] = user_message
        return context


class Message_show_view(LoginRequiredMixin, TemplateView):
    template_name = "system/message/widgets.html"
    model = Payam

    # form_class = PelanCreateForm

    def get_context_data(self, **kwargs):
        context = super(Message_show_view, self).get_context_data(**kwargs)
        payam = get_object_or_404(Payam, pk=self.kwargs['pk'])
        girande = None
        if payam.ferestande.id == self.request.user.id:
            girande = payam.girande
        elif payam.girande.id == self.request.user.id:
            girande = payam.ferestande

        all_message = Payam.objects.filter(ferestande=payam.ferestande, girande=payam.girande)

        send_message = Payam.objects.filter(ferestande=payam.ferestande, girande=payam.girande)
        get_message = Payam.objects.filter(ferestande=payam.girande, girande=payam.ferestande)
        ten_get_message = Payam.objects.filter(Q(girande=self.request.user, vazeyat=1))
        for i in ten_get_message:
            i.vazeyat = int(0)
            i.save()
        all_message = all_message.union(send_message, get_message).order_by('id')
        count_message = all_message.count()
        context['all_messsge'] = all_message
        context['count_message'] = count_message
        context['girande'] = girande
        context['ferestande'] = payam.ferestande
        return context


@csrf_exempt
def save_message(request):
    list = []
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        print("data", data)
        if data == "":
            data = "data"
            return HttpResponse()
        else:
            girande = data['girande']
            message = data['message']
            print("girande", girande)
            payam = Payam(ferestande=request.user, girande=User.objects.get(username=girande), onvan='chat',
                          text=message, vazeyat=1)
            payam.save()
            last_payam = Payam.objects.filter(ferestande=request.user,
                                              girande=User.objects.get(username=girande)).last()
            # print("last_payam",last_payam)
            last_pyam_messsage = last_payam.text

            return JsonResponse({"last_pyam_messsage": last_pyam_messsage}, safe=False)

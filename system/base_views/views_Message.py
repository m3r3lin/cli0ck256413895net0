from itertools import groupby
from django.forms import ModelForm, FileInput, Form
from django import forms
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import json
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from operator import itemgetter
from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, ListView,FormView,View
from system.models import Payam, Ticket, TicketMessages
from django.views.generic import TemplateView
from django.http import HttpResponse
from system.models import User
from system.forms import NewMessageCreateForm, CreateTicketForm
from django.db.models import Q
from django.contrib import messages

from system.templatetags.app_filters import date_jalali


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


class NewTicketCreateView(LoginRequiredMixin, FormView):
    template_name = 'system/message/Create_new_tickets.html'
    form_class = CreateTicketForm
    success_url = reverse_lazy('TicketListView')

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        message = form.cleaned_data.get('message')
        ticket=Ticket()
        ticket.title=title
        ticket.creator=self.request.user
        ticket.save()
        ticket_message=TicketMessages()
        ticket_message.ticket=ticket
        ticket_message.body=message
        ticket_message.creator=self.request.user
        if "file" in self.request.FILES:
            file = self.request.FILES.get('file')
            ticket_message.file=file
        ticket_message.save()
        messages.success(self.request, "تیکت شما با موفقیت ایجاد شد. لطفا از لیست تیکت ها ادامه کار را پیگیری کنید.")
        return super().form_valid(form)


class TicketListView(LoginRequiredMixin, TemplateView):
    template_name = 'system/message/List_Ticket.html'

class TicketDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = Ticket
    columns = ['id', 'title','date','status','unread_message']

    def get_initial_queryset(self):
        user = self.request.user
        qs = super().get_initial_queryset()
        if user.is_superuser:
            return qs
        qs = qs.filter(creator=user)
        return qs

    def render_column(self, row, column):
        if column == 'date':
            return date_jalali(row.date, 3)
        elif column =='unread_message':
            return TicketMessages.objects.filter(ticket=row,seen=False).count()
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(title__icontains=search))
        return qs

class ToggleTicketStateView(LoginRequiredMixin, View):
    def get(self, request, id):
        if not request.user.is_superuser:
            messages.error(request, _("You are not allowed to access"))
            return redirect("dashboard")
        try:
            ticket = Ticket.objects.get(id=id)
            ticket.status = not ticket.status
            ticket.save()
            if ticket.status:
                messages.success(request,"تیکت با موفقیت باز شد.")
            else:
                messages.success(request, "تیکت با موفقیت بسته شد.")
            return redirect("TicketListView")
        except:
            messages.error(request, "تیکت مورد نظر یافت نشد.")
            return redirect("TicketListView")


class ListTicketMessaesView(LoginRequiredMixin, View):
    def get(self, request, id):
        form = CreateTicketForm()
        del form.fields['title']
        ticket_id = forms.CharField(initial=id, widget=forms.HiddenInput())
        form.fields["ticket_id"] = ticket_id
        if not request.user.is_superuser:
            ticket = request.user.tickets.filter(id=id).first()
        else:
            ticket=Ticket.objects.filter(id=id).first()
        if ticket is None:
            return redirect(reverse_lazy("TicketListView"))
        messages = TicketMessages.objects.filter(ticket=ticket).update(seen=True)
        messages=TicketMessages.objects.filter(ticket=ticket).values('body', 'creator__username','file', 'date__date', 'date__time')
        logs = rows = groupby(messages, itemgetter('date__date'))
        messages= {c_title: list(items) for c_title, items in rows}
        return render(request,'system/message/List_TicketMessages.html',{'ticket_messages':messages,'form':form})
    def post(self,request,id):
        ticket_id=request.POST.get('ticket_id')
        print(ticket_id)
        if ticket_id:
            if ticket_id!=str(id):
                messages.error(request, _("You are not allowed to access"))
                return redirect("dashboard")
            else:
                if request.user.is_superuser:
                    ticket = Ticket.objects.filter(id=id).first()
                else:
                    ticket = request.user.tickets.filter(id=id).first()
                if ticket is None:
                    return redirect(reverse_lazy("TicketListView"))
                else:
                    ticket_message = TicketMessages()
                    ticket_message.ticket = ticket
                    ticket_message.body = request.POST.get('message')
                    ticket_message.creator = self.request.user
                    if "file" in self.request.FILES:
                        file = self.request.FILES.get('file')
                        ticket_message.file = file
                    ticket_message.save()
        else:
            messages.error(request, _("You are not allowed to access"))
            return redirect("dashboard")
        return redirect('ListTicketMessaes',id=id)
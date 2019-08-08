from django.db.models import Q

from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.utils.safestring import mark_safe
from django_datatables_view.base_datatable_view import BaseDatatableView
import simplejson as json
from system.models import User, HistoryIndirect
from django.db.models import Sum


class Chart_2_View(LoginRequiredMixin, TemplateView):
    template_name = "system/moshahede/chart_2.html"

    def get_context_data(self, *args, **kwargs):
        context = context = super().get_context_data(**kwargs)
        chart_config={
            'chart': {
                'container': "#OrganiseChart1",
                'rootOrientation': 'WEST',  # NORTH || EAST || WEST || SOUTH
                'scrollbar': "fancy",
                # 'levelSeparation': 30,
                'siblingSeparatio': 40,
                'subTeeSeparation': 80,
                'connectors': {
                    'type': 'step'
                },
                'node': {
                    'HTMLclass': 'nodeExample1'
                }
            }
        }
        user=self.request.user
        parrent=self.request.user.code_moaref
        print(parrent)
        if parrent is not None:
            chart_config['nodeStructure']={
                'text':{
                    'name': "دعوت کننده شما:",
                    'title': parrent.first_name + " " + parrent.last_name
                },
                'image': "/static/img/avatar/avatar.png",
                'children': []
            }
        else:
            chart_config['nodeStructure'] = {
                'text': {
                    'name':user.first_name + ' ' + user.last_name ,
                    'title': "شما در سطح یک قرار دارید"
                },
                'image': "/static/img/avatar/avatar.png",
                'children': []
            }
        print(chart_config)
        context['chart_config'] = mark_safe(str(chart_config))
        return context

class Chart_1_View(LoginRequiredMixin, TemplateView):
    template_name = "system/moshahede/parent_children.html"

class ParentChildrenDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = User
    columns = ['first_name','sath','daramad']

    def get_initial_queryset(self):
        user=self.request.user
        qs = super().get_initial_queryset()
        qs = qs.filter(list_parent__contains="[{}]".format(user.id))
        return qs

    def render_column(self, row:User, column):
        jsonDec = json.decoder.JSONDecoder()
        parents = jsonDec.decode(row.list_parent)
        if column == 'first_name':
            return row.first_name + " " +row.last_name
        if column =='sath':
            return parents.index([self.request.user.id])+1
        if column =="daramad":
            history=HistoryIndirect.objects.filter(parent=self.request.user,montasher_konande=row).all().aggregate(Sum('mablagh'))
            return history['mablagh__sum']
        return super().render_column(row, column)


class Parent_Children_List_View(LoginRequiredMixin, ListView):
    model = User
    template_name = 'system/moshahede/list_of_parent_children.html'

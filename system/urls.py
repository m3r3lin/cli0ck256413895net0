from django.urls import path

from system.base_views.views_Pelan import PelanCreateView, PelanUpdateView, PelanDeleteView, PelanListView, PelanDatatableView, PlanReportsView
from system.base_views.views_Tabligh import TablighCreateView, TablighUpdateView, TablighDeleteView, TablighListView, TablighDatatableView
from system.base_views.views_Tanzimat_Paye import ActiveCodeMoarefView, SodeModirView
from system.base_views.views_User import UserCreateView, UserUpdateView, login_user, logout_user, UserListView, UserDeleteView, UserDatatableView, UserCreateModirView, ChangeUserPasswordView
from system.views import Dashboard

urlpatterns = [
    path('login/', login_user, name='login'),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
    path('logout/', logout_user, name='logout'),
    path('CreateUser/', UserCreateView.as_view(), name='CreateUser'),
    path('CreateUserModir/', UserCreateModirView.as_view(), name='CreateUserModir'),
    path('UpdateUser/<int:pk>', UserUpdateView.as_view(), name='UpdateUser'),
    path('DeleteUser/<int:pk>', UserDeleteView.as_view(), name='DeleteUser'),
    path('ListUser/', UserListView.as_view(), name='ListUser'),
    path('UserDatatable/', UserDatatableView.as_view(), name='UserDatatable'),
    path('ChangeUserPassword/', ChangeUserPasswordView.as_view(), name='ChangeUserPassword'),
    # ---- Pelan
    path('CreatePelan/', PelanCreateView.as_view(), name='CreatePelan'),
    path('UpdatePelan/<int:pk>', PelanUpdateView.as_view(), name='UpdatePelan'),
    path('DeletePelan/<int:pk>', PelanDeleteView.as_view(), name='DeletePelan'),
    path('ListPelan/', PelanListView.as_view(), name='ListPelan'),
    path('PelanDatatable/', PelanDatatableView.as_view(), name='PelanDatatable'),
    path('PlanReports/', PlanReportsView.as_view(), name='PelanReportDatatable'),
    # ---- Tabligh
    path('CreateTabligh/', TablighCreateView.as_view(), name='CreateTabligh'),
    path('UpdateTabligh/<int:pk>', TablighUpdateView.as_view(), name='UpdateTabligh'),
    path('DeleteTabligh/<int:pk>', TablighDeleteView.as_view(), name='DeleteTabligh'),
    path('ListTabligh/', TablighListView.as_view(), name='ListTabligh'),
    path('TablighDatatable/', TablighDatatableView.as_view(), name='TablighDatatable'),
    # ---- TanzimatPaye
    path('ActiveCodeMoaref/', ActiveCodeMoarefView.as_view(), name='ActiveCodeMoaref'),
    path('SodeModir/', SodeModirView.as_view(), name='SodeModir'),
]

from django.urls import path

# from system.base_views import views_Message
from system.base_views import views_Message
from system.base_views.views_Click import ClickedOnTablighView
from system.base_views.views_Malli import IncreaseBalanceView, dargah_test_part_1
from system.base_views.views_Message import MessageListview, Message_show_view
from system.base_views.views_Message import NewMessageCreateView
from system.base_views.views_Pelan import PelanCreateView, PelanUpdateView, PelanDeleteView, PelanListView, PelanDatatableView, PlanReportsView
from system.base_views.views_Tabligh import TablighCreateView, TablighUpdateView, TablighDeleteView, TablighListView, TablighDatatableView, PublishShowView, TablighPreviewView, PublishTablighView, MotashershodeDatatableView, Montashshodeha
from system.base_views.views_Tanzimat_Paye import ActiveCodeMoarefView, SodeModirView, MaxCountNetworkLevel
from system.base_views.views_Tanzimat_Paye import Languge_siteView, Count_Level_networkView, Count_kharid_hadaghalView, Time_kharid_termView, \
    Taien_meghdar_matlabView, Show_amar_foruserView, Taeid_khodkar_tablighView,Vahed_poll_siteView,Count_visit_tablighView,Taein_hadaghal_etbarView,\
    Amar_jaali_View,Count_Level_networkDataTableView,Count_Level_networkDeleteView,Count_Level_networkUpdateView
from system.base_views.views_User import RedirectToUserUpdate
from system.base_views.views_User import UserCreateView, UserUpdateView, login_user, logout_user, UserListView, UserDeleteView, UserDatatableView, ChangeUserPasswordView, \
    ProfileUserView
from system.views import Dashboard

urlpatterns = [
    path('login/', login_user, name='login'),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
    path('logout/', logout_user, name='logout'),
    path('CreateUser/', UserCreateView.as_view(), name='CreateUser'),
    path('UpdateUser/<int:pk>', UserUpdateView.as_view(), name='UpdateUser'),
    path('UpdateUser/', RedirectToUserUpdate.as_view(), name='UpdateUser'),
    path('DeleteUser/<int:pk>', UserDeleteView.as_view(), name='DeleteUser'),
    path('ListUser/', UserListView.as_view(), name='ListUser'),
    path('UserDatatable/', UserDatatableView.as_view(), name='UserDatatable'),
    path('ChangeUserPassword/', ChangeUserPasswordView.as_view(), name='ChangeUserPassword'),
    path('ProfileUser/', ProfileUserView.as_view(), name='ProfileUser'),
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
    path('EntesharDatatable/', MotashershodeDatatableView.as_view(), name='MontashshodeDatatable'),
    path('PreviewTabligh/<tabligh_token>', TablighPreviewView.as_view(), name='PreviewTabligh'),
    path('PublishTabligh/<tabligh_token>', PublishTablighView.as_view(), name='PublishTabligh'),
    path('PublishShow/', PublishShowView.as_view(), name='ShowTablighs'),
    path('Montashshodeha/', Montashshodeha.as_view(), name='Montashshodeha'),
    # ---- TanzimatPaye
    path('ActiveCodeMoaref/', ActiveCodeMoarefView.as_view(), name='ActiveCodeMoaref'),
    path('TedadSathShabake/', Count_Level_networkView.as_view(), name='TedadSathShabake'),
    path('SodeModir/', SodeModirView.as_view(), name='SodeModir'),
    path('Languge_site/', Languge_siteView.as_view(), name='Languge_site'),
    #datatable count level network
    path('Count_Level_networkDataTable/', Count_Level_networkDataTableView.as_view(), name='Count_Level_networkDataTable'),
    path('Count_Level_networkDelete/<int:pk>', Count_Level_networkDeleteView.as_view(), name='Count_Level_networkDelete'),
    path('Count_Level_networkUpdate/<int:pk>', Count_Level_networkUpdateView.as_view(), name='Count_Level_networkUpdate'),
    path('Count_Level_networkView/', Count_Level_networkView.as_view(), name='Count_Level_networkView'),
    path('Max_Count_Level_networkView/', MaxCountNetworkLevel.as_view(), name='Max_Count_Level_networkView'),
    path('Count_kharid_hadaghalView/', Count_kharid_hadaghalView.as_view(), name='Count_kharid_hadaghalView'),
    path('Time_kharid_termView/', Time_kharid_termView.as_view(), name='Time_kharid_termView'),
    path('Taien_meghdar_matlabView/', Taien_meghdar_matlabView.as_view(), name='Taien_meghdar_matlabView'),
    path('Show_amar_foruserView/', Show_amar_foruserView.as_view(), name='Show_amar_foruserView'),
    path('Taeid_khodkar_tabligh/', Taeid_khodkar_tablighView.as_view(), name='Taeid_khodkar_tabligh'),
    path('Vahed_poll_site/', Vahed_poll_siteView.as_view(), name='Vahed_poll_site'),
    path('Count_visit_tabligh/', Count_visit_tablighView.as_view(), name='Count_visit_tabligh'),
    path('Count_visit_tabligh/', Count_visit_tablighView.as_view(), name='Count_visit_tabligh'),
    path('Taein_hadaghal_etbar/', Taein_hadaghal_etbarView.as_view(), name='Taein_hadaghal_etbar'),
    path('Amar_jaali/', Amar_jaali_View.as_view(), name='Amar_jaali'),
    # ---- messages
    path('MessageList/', MessageListview.as_view(), name='MessageList'),
    path('Message_show_view/<int:pk>', Message_show_view.as_view(), name='Message_show_view'),
    path('NewMessageCreate/', NewMessageCreateView.as_view(), name='NewMessageCreate'),
    # ---- ajax
    path('save_message/', views_Message.save_message, name='save_message'),
    # ---- MALLI
    path('increase_balance/', IncreaseBalanceView.as_view(), name='increase_balance'),
    path('virtual_bank_verification1/', dargah_test_part_1),
    # ---- Click
    path('click/<enteshartoken>',ClickedOnTablighView.as_view(),name='clicked_on_tabligh'),
]

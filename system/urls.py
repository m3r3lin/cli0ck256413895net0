from django.urls import path
# from system.base_views import views_Message
from system.base_views import views_Message


from system.base_views.views_Pelan import PelanCreateView, PelanUpdateView, PelanDeleteView, PelanListView, PelanDatatableView, PlanReportsView
from system.base_views.views_Tabligh import TablighCreateView, TablighUpdateView, TablighDeleteView, TablighListView, TablighDatatableView
from system.base_views.views_Tanzimat_Paye import ActiveCodeMoarefView, SodeModirView,\
    Languge_siteView,Count_Level_networkView,Count_kharid_hadaghalView,Time_kharid_termView,Taien_meghdar_matlabView,\
    Show_amar_foruserView,Taeid_khodkar_tablighView
from system.base_views.views_User import UserCreateView, UserUpdateView, login_user, logout_user, UserListView, UserDeleteView, UserDatatableView, UserCreateModirView
from system.base_views.views_Message import MessageListview,Message_show_view
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
    path('Languge_site/', Languge_siteView.as_view(), name='Languge_site'),
    path('Count_Level_networkView/', Count_Level_networkView.as_view(), name='Count_Level_networkView'),
    path('Count_kharid_hadaghalView/', Count_kharid_hadaghalView.as_view(), name='Count_kharid_hadaghalView'),
    path('Time_kharid_termView/', Time_kharid_termView.as_view(), name='Time_kharid_termView'),
    path('Taien_meghdar_matlabView/', Taien_meghdar_matlabView.as_view(), name='Taien_meghdar_matlabView'),
    path('Show_amar_foruserView/', Show_amar_foruserView.as_view(), name='Show_amar_foruserView'),
    path('Taeid_khodkar_tabligh/', Taeid_khodkar_tablighView.as_view(), name='Taeid_khodkar_tabligh'),

    #messages
    path('MessageList/', MessageListview.as_view(), name='MessageList'),
    path('Message_show_view/<int:pk>', Message_show_view.as_view(), name='Message_show_view'),
    #ajax
    path('save_message/', views_Message.save_message, name='save_message'),

]
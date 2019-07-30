from django.urls import path

from system.base_views.views_Pelan import PelanCreateView, PelanUpdateView, PelanDeleteView, PelanListView
from system.base_views.views_Tabligh import TablighCreateView, TablighUpdateView, TablighDeleteView, TablighListView
from system.base_views.views_User import UserCreateView, UserUpdateView, login_user, logout_user, UserListView, UserDeleteView
from system.views import Dashboard

urlpatterns = [
    path('CreateUser/', UserCreateView.as_view(), name='CreateUser'),
    # path('UpdateUser/', UserUpdateView.as_view(), name='UpdateUser'),
    path('UpdateUser/<int:pk>', UserUpdateView.as_view(), name='UpdateUser'),
    path('DeleteUser/<int:pk>', UserDeleteView.as_view(), name='DeleteUser'),
    path('ListUser/', UserListView.as_view(), name='ListUser'),
    path('login/', login_user, name='login'),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
    path('logout/', logout_user, name='logout'),
    # ---- Pelan
    path('CreatePelan/', PelanCreateView.as_view(), name='CreatePelan'),
    path('UpdatePelan/<int:pk>', PelanUpdateView.as_view(), name='UpdatePelan'),
    path('DeletePelan/<int:pk>', PelanDeleteView.as_view(), name='DeletePelan'),
    path('ListPelan/', PelanListView.as_view(), name='ListPelan'),
    # ---- Tabligh
    path('CreateTabligh/', TablighCreateView.as_view(), name='CreateTabligh'),
    path('UpdateTabligh/<int:pk>', TablighUpdateView.as_view(), name='UpdateTabligh'),
    path('DeleteTabligh/<int:pk>', TablighDeleteView.as_view(), name='DeleteTabligh'),
    path('ListTabligh/', TablighListView.as_view(), name='ListTabligh'),
]

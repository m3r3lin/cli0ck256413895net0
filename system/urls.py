from django.urls import path

from system.base_views.views_Pelan import PelanCreateView, PelanUpdateView, PelanDeleteView, PelanListView
from system.base_views.views_User import UserCreateView, UserUpdateView, login_user, logout_user
from system.views import Dashboard

urlpatterns = [
    path('CreateUser/', UserCreateView.as_view(), name='CreateUser'),
    path('UpdateUser/', UserUpdateView.as_view(), name='UpdateUser'),
    path('login/', login_user, name='login'),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
    path('logout/', logout_user, name='logout'),
    # ---- Pelan
    path('CreatePelan/', PelanCreateView.as_view(), name='CreatePelan'),
    path('UpdatePelan/<int:pk>', PelanUpdateView.as_view(), name='UpdatePelan'),
    path('DeletePelan/<int:pk>', PelanDeleteView.as_view(), name='DeletePelan'),
    path('ListPelan/', PelanListView.as_view(), name='ListPelan'),
]

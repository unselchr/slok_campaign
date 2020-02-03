from django.urls import path
from . import views

urlpatterns = [
    path('', views.RosterListView.as_view(), name='roster-list')
]

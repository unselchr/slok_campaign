from django.urls import path
from . import views

app_name = 'roster'
urlpatterns = [
    path('', views.RosterListView.as_view(), name='roster_list')
]

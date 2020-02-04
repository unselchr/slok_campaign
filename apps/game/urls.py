from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path('', views.GameListView.as_view(), name='game_list'),
    path('<pk>/', views.GameDetailView.as_view(), name='game_detail'),
]

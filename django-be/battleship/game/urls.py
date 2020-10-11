from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('<str:game_id>/start', views.start_game, name='start_game'),
    path('<str:game_id>/attack', views.attack, name='attack'),
    path('<str:game_id>/', views.launch_game, name='launch_game')
]

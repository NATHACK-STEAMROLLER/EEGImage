from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('generate', views.generate, name='generate'),
    path('', views.start_page, name='start_page'),
    path('countdown/', views.countdown_page, name='countdown_page'),
    path('history/', views.history, name='history'),
]
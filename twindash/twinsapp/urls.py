from django.urls import path

from . import views

app_name = 'twinsapp'
urlpatterns = [
    path('', views.index, name='index'),
    # ex. /twinsapp/MAIA/
    path('<nombre_bebe>/', views.main_bebe, name='main_bebe'),
    # ex. /twinsapp/MAIA/2020/03/01/
    path('<nombre_bebe>/<int:year>/<int:month>/<int:day>/', views.bebe_dia, name='bebe_dia'),
    path('^tomas/$', views.resumen_tomas, name='resumen_tomas'),
]

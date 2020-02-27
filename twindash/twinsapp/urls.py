from django.urls import path

from . import views

app_name = 'twinsapp'
urlpatterns = [
    path('', views.index, name='index'),
    # ex. /twinsapp/bebe/MAIA/
    path('bebe/<nombre_bebe>/', views.main_bebe, name='main_bebe'),
    # ex. /twinsapp/2020/02/17/
    path('<int:year>/<int:month>/<int:day>/', views.detail_day, name='detail_day')
]

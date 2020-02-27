from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Bebe, Toma, Cambio

import datetime


# Create your views here.
@login_required(login_url='/admin/login/')
def index(request):
    ultimas_tomas = Toma.objects.order_by("-fecha")[:10]
    ultimos_cambios = Cambio.objects.order_by("-fecha")[:10]
    lista_bebes = Bebe.objects.all()
    context = {
        'latest_tomas_list': ultimas_tomas,
        'latest_cambios_list': ultimos_cambios,
        'bebe_list': lista_bebes
        }
    return render(request, 'twinsapp/index.html', context)


@login_required(login_url='/admin/login/')
def main_bebe(request, nombre_bebe):
    bebe = get_object_or_404(Bebe, nombre=nombre_bebe)
    return HttpResponse("You are looking at main landing page for bebe {}, with id {}"
                        .format(bebe.nombre, bebe.id))


@login_required(login_url='/admin/login/')
def detail_day(request, year, month, day):
    date = datetime.date(year, month, day)
    tomas_dia = Toma.objects.filter(fecha__date=date)
    output = "<br> ".join([str(t) for t in tomas_dia])
    return HttpResponse(output)

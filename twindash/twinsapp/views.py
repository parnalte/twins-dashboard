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
    lista_bebes = Bebe.objects.all()
    dia_hoy = datetime.date.today()

    tomas_bebe_hoy = Toma.objects.filter(fecha__date=dia_hoy, bebe = bebe)
    n_tomas_hoy = tomas_bebe_hoy.count()
    cantidad_bibe_hoy = (
        sum([x['cantidad_artificial'] for x in tomas_bebe_hoy.values()]) +
        sum([x['cantidad_materna'] for x in tomas_bebe_hoy.values()]) )
    n_tomas_teta_hoy = tomas_bebe_hoy.filter(toma_teta=True).count()

    cambios_bebe_hoy = Cambio.objects.filter(fecha__date=dia_hoy, bebe = bebe)
    n_cambios_hoy = cambios_bebe_hoy.count()
    ultimo_cambio_caca = Cambio.objects.filter(caca=True, bebe=bebe).order_by("fecha").last()

    context = {
        'bebe': bebe,
        'bebe_list': lista_bebes,
        'hoy': dia_hoy,
        'latest_tomas_list': tomas_bebe_hoy,
        'n_tomas': n_tomas_hoy,
        'cantidad_bibe': cantidad_bibe_hoy,
        'n_tomas_teta': n_tomas_teta_hoy,
        'latest_cambios_list': cambios_bebe_hoy,
        'n_cambios': n_cambios_hoy,
        'ultima_caca': ultimo_cambio_caca,
    }
    return render(request, 'twinsapp/bebe.html', context)


@login_required(login_url='/admin/login/')
def detail_day(request, year, month, day):
    date = datetime.date(year, month, day)
    tomas_dia = Toma.objects.filter(fecha__date=date)
    output = "<br> ".join([str(t) for t in tomas_dia])
    return HttpResponse(output)

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Bebe, Toma, Cambio
from .plots import plot_resumen_tomas, plot_bebe_dia

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
def bebe_dia(request, nombre_bebe, year, month, day):
    bebe = get_object_or_404(Bebe, nombre=nombre_bebe)
    lista_bebes = Bebe.objects.all()
    fecha = datetime.date(year, month, day)
    dia_hoy = datetime.date.today()

    tomas_bebe_hoy = Toma.objects.filter(fecha__date=fecha, bebe = bebe).order_by("-fecha")
    n_tomas_hoy = tomas_bebe_hoy.count()
    cantidad_bibe_hoy = (
        sum([x['cantidad_artificial'] for x in tomas_bebe_hoy.values()]) +
        sum([x['cantidad_materna'] for x in tomas_bebe_hoy.values()]) )
    n_tomas_teta_hoy = tomas_bebe_hoy.filter(toma_teta=True).count()

    cambios_bebe_hoy = Cambio.objects.filter(fecha__date=fecha, bebe = bebe).order_by("-fecha")
    n_cambios_hoy = cambios_bebe_hoy.count()
    n_cambios_hoy_caca = cambios_bebe_hoy.filter(caca=True).count()
    ultimo_cambio_caca = Cambio.objects.filter(caca=True, bebe=bebe).order_by("fecha").last()

    es_hoy = (fecha == dia_hoy)
    fecha_anterior = fecha - datetime.timedelta(days=1)
    fecha_posterior = fecha + datetime.timedelta(days=1)

    script_plot, div_plot = plot_bebe_dia(bebe, fecha)

    context = {
        'bebe': bebe,
        'bebe_list': lista_bebes,
        'fecha': fecha,
        'es_hoy': es_hoy,
        'fecha_anterior': fecha_anterior,
        'fecha_posterior': fecha_posterior,
        'latest_tomas_list': tomas_bebe_hoy,
        'n_tomas': n_tomas_hoy,
        'cantidad_bibe': cantidad_bibe_hoy,
        'n_tomas_teta': n_tomas_teta_hoy,
        'latest_cambios_list': cambios_bebe_hoy,
        'n_cambios': n_cambios_hoy,
        'n_cambios_caca': n_cambios_hoy_caca,
        'ultima_caca': ultimo_cambio_caca,
        'script_plot': script_plot,
        'div_plot': div_plot,
    }
    return render(request, 'twinsapp/bebe_dia.html', context)


@login_required(login_url='/admin/login/')
def main_bebe(request, nombre_bebe):
    dia_hoy = datetime.date.today()
    return bebe_dia(request, nombre_bebe, dia_hoy.year, dia_hoy.month, dia_hoy.day)

@login_required(login_url='/admin/login/')
def resumen_tomas(request):
    lista_bebes = Bebe.objects.all()
    script_plot, div_plot = plot_resumen_tomas()
    context = {
        'bebe_list': lista_bebes,
        'script_plot': script_plot,
        'div_plot': div_plot,
    }
    return render(request, 'twinsapp/resumen_tomas.html', context)

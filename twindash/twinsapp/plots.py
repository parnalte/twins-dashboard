import pandas as pd
import numpy as np
import datetime

import bokeh.plotting as bplot
from bokeh.models import DatetimeTickFormatter
from bokeh.embed import components

from .models import Toma

def plot_resumen_tomas():

    # Get all tomas as dataframe
    qs_maia = Toma.objects.filter(bebe__nombre="MAIA")
    tomas_maia = pd.DataFrame.from_records(qs_maia.values())
    qs_vega = Toma.objects.filter(bebe__nombre="VEGA")
    tomas_vega = pd.DataFrame.from_records(qs_vega.values())

    tomas_maia['cantidad_total'] = tomas_maia['cantidad_artificial'] + tomas_maia['cantidad_materna']
    df_maia = tomas_maia[['fecha', 'cantidad_total']].set_index('fecha').resample('D').sum()

    tomas_vega['cantidad_total'] = tomas_vega['cantidad_artificial'] + tomas_vega['cantidad_materna']
    df_vega = tomas_vega[['fecha', 'cantidad_total']].set_index('fecha').resample('D').sum()

    # create a new plot with a title and axis labels
    p = bplot.figure(x_axis_label='Día',
                    y_axis_label='Cantidad bibes (ml)', x_axis_type="datetime",
                    plot_width=900, plot_height=350,
                    sizing_mode='scale_width')

    # add a line renderer with legend and line thickness
    p.line(x=df_maia.index, y=df_maia["cantidad_total"], legend_label="MAIA",
           line_color='khaki', line_width=3)
    p.line(x=df_vega.index, y=df_vega["cantidad_total"], legend_label="VEGA",
          line_color='darkmagenta', line_width=3)

    p.xaxis[0].formatter = DatetimeTickFormatter(days=["%a %d %b"])

    script, div = components(p)

    return script, div

# Utility function
def resample_day_data(qs, date):
    qs_day = qs.filter(fecha__date = date)
    tomas_day = pd.DataFrame.from_records(qs_day.values('fecha', 'cantidad_artificial'))

    fake_rows = pd.DataFrame()
    fake_rows['fecha'] = [datetime.datetime(date.year, date.month, date.day, 0, 0),
                          datetime.datetime(date.year, date.month, date.day, 23, 59)]
    fake_rows['cantidad_artificial'] = [0, 0]

    tomas_day_res = tomas_day.append(fake_rows,  ignore_index=True).set_index('fecha').resample('5Min').sum()
    tomas_day_cumsum = tomas_day_res.cumsum()
    tomas_day_cumsum[tomas_day_cumsum.index > datetime.datetime.now()] = np.nan
    return tomas_day_cumsum


def plot_bebe_dia(bebe, fecha):

    qs_tomas = Toma.objects.filter(bebe = bebe)

    # Get data for the given day
    tomas_day = pd.DataFrame.from_records(qs_tomas.filter(fecha__date = fecha).values())
    tomas_day_cumulative = resample_day_data(qs_tomas, fecha)

    # Get data for the previous 5 days
    tomas_previous = pd.DataFrame(index=tomas_day_cumulative.index)
    for tdiff in range(1,6):
        pdate = fecha- datetime.timedelta(days=tdiff)
        tcum_pdate = resample_day_data(qs_tomas, pdate)
        tcum_pdate.index = tcum_pdate.index + datetime.timedelta(days=tdiff)
        tomas_previous[tdiff] = tcum_pdate

    # Now, crete the plot
    p = bplot.figure(x_axis_label='Hora', y_axis_label='Cantidad bibes (ml)',
                     x_axis_type="datetime", plot_width=900, plot_height=350,
                     sizing_mode='scale_width')

    p.line(x=tomas_previous.index,
           y=tomas_previous.mean(axis=1),
           line_width=1, color='gray',
           legend_label="Media 5 días anteriores ({:g} ml)".format(tomas_previous.mean(axis=1)[-1]))

    p.varea(x=tomas_previous.index,
            y1=tomas_previous.max(axis=1),
            y2=tomas_previous.min(axis=1),
            color='gray', alpha=0.3)

    p.line(x=tomas_day_cumulative.index,
           y=tomas_day_cumulative["cantidad_artificial"],
           line_width=5, color='green',
           legend_label="{} ({:g} ml)".format(fecha.strftime("%a, %d/%m/%y"),
                    tomas_day_cumulative['cantidad_artificial'].max(skipna=True)))

    # In case there are no tomas in this day
    try:
        p.vbar(x=tomas_day['fecha'], top=tomas_day["cantidad_artificial"],
               width=datetime.timedelta(minutes=20), alpha=0.6, color='green', )
    except:
        pass

    p.xaxis[0].formatter = DatetimeTickFormatter(hours=["%H:%M"], days=["%H:%M"])
    p.legend.location = "top_left"

    script, div = components(p)

    return script, div

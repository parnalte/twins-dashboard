import pandas as pd

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

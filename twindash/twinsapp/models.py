from django.db import models

# Create your models here.
class Bebe(models.Model):
    nombre = models.CharField("Nombre de la bebé", max_length=80, unique=True)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Bebé"

class Toma(models.Model):
    bebe = models.ForeignKey(Bebe, on_delete=models.CASCADE)
    fecha = models.DateTimeField("Fecha y hora de la toma")
    cantidad_artificial = models.FloatField("Cantidad leche artificial", default=0)
    cantidad_materna = models.FloatField("Cantidad leche materna (bibe)", default=0)
    toma_teta = models.BooleanField("Ha tomado teta?", default=False)
    VALORES_TETA = [
        (0, '0 - Nada'),
        (1, '1 - Muy poco'),
        (2, '2 - Poco'),
        (3, '3 - Normal'),
        (4, '4 - Bastante'),
        (5, '5 - Mucho'),
    ]
    valor_teta = models.IntegerField("Cantidad teta", blank=True, null=True,
                                     choices=VALORES_TETA)
    comentario = models.CharField("Comentario", max_length=300, blank=True, null=True)

    def __str__(self):
        out = self.bebe.nombre + ": " + self.fecha.strftime('%a, %d/%m/%Y -- %H:%M: ')
        if self.cantidad_artificial > 0:
            out += "{:g}A  ".format(self.cantidad_artificial)
        if self.cantidad_materna > 0:
            out += "{:g}M  ".format(self.cantidad_materna)
        if self.toma_teta:
            out += "+ Teta ({}) ".format(self.valor_teta)
        if self.comentario is not None:
            out += "[" + self.comentario + "]"

        return out

class Cambio(models.Model):
    bebe = models.ForeignKey(Bebe, on_delete=models.CASCADE)
    fecha = models.DateTimeField("Fecha y hora del cambio")
    pipi = models.BooleanField("Pipí", default=False)
    caca = models.BooleanField("Caca", default=False)
    comentario = models.CharField("Comentario", max_length=300, blank=True, null=True)

    def __str__(self):
        out = self.bebe.nombre + ": " + self.fecha.strftime('%a, %d/%m/%Y -- %H:%M: ')
        if self.pipi:
            out += "Pipí"
        if self.caca:
            out += " + Caca"
        if self.comentario is not None:
            out += " [" + self.comentario + "]"

        return out

    class Meta:
        verbose_name = "Cambio de pañal"
        verbose_name_plural = "Cambios de pañal"

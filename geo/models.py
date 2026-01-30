from django.db import models


def default_alternative_names():
    return []


class State(models.Model):
    inegi_code = models.CharField(max_length=2, verbose_name="Clave INEGI")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    short_name = models.CharField(
        max_length=20, verbose_name="Nombre Corto",
        blank=True, null=True)
    code_name = models.CharField(
        max_length=6, verbose_name="Nombre Clave",
        blank=True, null=True)
    alternative_names = models.JSONField(
        default=default_alternative_names,
        verbose_name="Lista nombres alternativos",
        help_text="Ocupar para OCAMIS",
    )

    def __str__(self):
        return self.short_name or self.code_name or self.name

    class Meta:
        ordering = ["inegi_code"]
        verbose_name = "Entidad Federativa"
        verbose_name_plural = "Entidades Federativas"


class HealthDistrict(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='health_districts')

    class Meta:
        verbose_name = 'health_district'

    def __str__(self):
        return self.name


class Municipality(models.Model):

    inegi_code = models.CharField(max_length=6, verbose_name="Clave INEGI")
    state = models.ForeignKey(
        State, verbose_name="State",
        null=True, on_delete=models.CASCADE,
        related_name="municipalities")
    complete_code = models.CharField(
        max_length=8, verbose_name="Clave INEGI Completa")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    health_district = models.ForeignKey(
        HealthDistrict, on_delete=models.CASCADE,
        related_name='municipalities')
    std_name = models.CharField(
        max_length=255, verbose_name="Nombre Estandarizado")
    population = models.IntegerField(
        blank=True, null=True, verbose_name="Población")
    latitude = models.FloatField(
        blank=True, null=True, verbose_name="Latitud de cabecera")
    longitude = models.FloatField(
        blank=True, null=True, verbose_name="Longitud de cabecera")
    altitude = models.IntegerField(
        blank=True, null=True, verbose_name="Altitud de cabecera")

    def __str__(self):
        return "%s - %s" % (self.name, self.state)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ["inegi_code"]


class Locality(models.Model):
    inegi_code = models.CharField(max_length=6, verbose_name="Clave INEGI")
    complete_code = models.CharField(
        max_length=12, verbose_name="Clave INEGI Completa")
    name = models.CharField(max_length=120, verbose_name="Nombre")
    municipality = models.ForeignKey(
        Municipality, verbose_name="Municipality",
        null=True, on_delete=models.CASCADE, related_name="localities")
    population = models.IntegerField(
        blank=True, null=True, verbose_name="Población")
    is_rural = models.BooleanField(default=False, verbose_name="Es rural")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.municipality)

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"

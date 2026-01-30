import uuid as uuid_lib

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from category.models import AgentType
from geo.models import State, HealthDistrict, Municipality
from gob.models import Institution


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    can_edit = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    full_editor = models.BooleanField(
        default=False, verbose_name='Es capturista',
        help_text='Puede agregar notas, comentarios a los registros,'
                  'pero no tiene todos los permisos')


    class Meta:
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuarios'

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_super_user', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default='')
    last_name2 = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, default='')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='users')
    health_district = models.ForeignKey(
        HealthDistrict, on_delete=models.CASCADE, related_name='users')
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name='users')
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    password_changed = models.BooleanField(
        default=False, verbose_name='Contraseña cambiada')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    @property
    def is_full_editor(self):
        if self.is_anonymous:
            return False
        return self.is_superuser or self.is_staff or self.full_editor

    @property
    def is_admin(self):
        if self.is_anonymous:
            return False
        return self.is_superuser or self.is_staff

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name or self.last_name:
            return f"{self.first_name or self.last_name}"
        return self.username or self.email

    def __str__(self):
        return self.email


class Agent(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default='')
    last_name2 = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True, related_name='agents')
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='agents')
    community = models.CharField(max_length=255, null=True, blank=True)
    agent_type = models.ForeignKey(AgentType, on_delete=models.CASCADE, related_name='agents')
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='agents')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Agente comunitario de salud'
        verbose_name_plural = 'Agentes comunitarios de salud'

    def __str__(self):
        return f"{self.name} {self.last_name}"


class InvitationToken(models.Model):
    key = models.UUIDField(
        primary_key=True, default=uuid_lib.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="Correo electrónico", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Creado")
    viewed_at = models.DateTimeField(
        verbose_name="Fecha en que se vio", blank=True, null=True)
    used_at = models.DateTimeField(
        verbose_name="Fecha en que se usó",
        blank=True, null=True)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Token de Invitación"
        verbose_name_plural = "Tokens de Invitación"

    def __str__(self):
        return "%s - %s" % (self.institution, self.key)

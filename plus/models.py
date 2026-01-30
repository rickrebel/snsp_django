from django.db import models
from django.utils import timezone
from geo.models import (
    State, Municipality, Locality, HealthDistrict)
from user.models import User, Agent
from gob.models import Institution, Program
from category.models import StatusControl, PriorityGroup, PlaceType


class Community(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE,
        related_name='communities')
    health_district = models.ForeignKey(
        HealthDistrict, on_delete=models.CASCADE,
        related_name='communities')
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE,
        related_name='communities')
    locality = models.ForeignKey(
        Locality, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='communities')
    place_type = models.ForeignKey(
        PlaceType, on_delete=models.CASCADE, related_name='communities')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'community'
        verbose_name_plural = 'Communities'

    def __str__(self):
        return self.name or f"Community {self.id}"


class HealthMeeting(models.Model):
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE,
        related_name='health_meetings')
    person_count = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='health_meetings_created')
    date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    participants = models.ManyToManyField(
        User, related_name='health_meetings', blank=True)
    agents = models.ManyToManyField(
        Agent, related_name='health_meetings', blank=True)
    institutions = models.ManyToManyField(
        Institution, related_name='health_meetings', blank=True)
    conveners = models.ManyToManyField(
        Institution, related_name='convened_meetings', blank=True)

    class Meta:
        verbose_name = 'Junta Comunitaria'
        verbose_name_plural = 'Juntas Comunitarias'

    def __str__(self):
        return f"Health Meeting {self.id} - {self.date}"


class Goal(models.Model):
    description = models.TextField()
    health_meeting = models.ForeignKey(
        HealthMeeting, on_delete=models.CASCADE, related_name='goals')
    status = models.ForeignKey(
        StatusControl, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='goals')

    responsibles = models.ManyToManyField(
        Institution, related_name='responsible_goals', blank=True)

    class Meta:
        verbose_name = 'goal'

    def __str__(self):
        return f"Goal {self.id}"


class IntensiveDay(models.Model):
    comment = models.TextField(null=True, blank=True)
    person_count = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='intensive_days_created')
    date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    participants = models.ManyToManyField(
        User, related_name='intensive_days', blank=True)
    agents = models.ManyToManyField(
        Agent, related_name='intensive_days', blank=True)
    communities = models.ManyToManyField(
        Community, related_name='intensive_days', blank=True)
    priority_groups = models.ManyToManyField(
        PriorityGroup, related_name='intensive_days', blank=True)
    institutions = models.ManyToManyField(
        Institution, related_name='intensive_days', blank=True)

    class Meta:
        verbose_name = 'intensive_day'

    def __str__(self):
        return f"Intensive Day {self.id} - {self.date}"


class ProgressAdvance(models.Model):
    comment = models.TextField(null=True, blank=True)
    status_goal = models.ForeignKey(
        StatusControl, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='progress_advances')
    intensive_day = models.ForeignKey(
        IntensiveDay, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='progress_advances')

    class Meta:
        verbose_name = 'progress_advance'

    def __str__(self):
        return f"Progress Advance {self.id}"


class PriorityAction(models.Model):
    comment = models.TextField(null=True, blank=True)
    beneficiaries = models.IntegerField(null=True, blank=True)
    program = models.ForeignKey(
        Program, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='priority_actions')
    intensive_day = models.ForeignKey(
        IntensiveDay, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='priority_actions')

    class Meta:
        verbose_name = 'priority_action'

    def __str__(self):
        return f"Priority Action {self.id}"


class Assistant(models.Model):
    intensive_day = models.ForeignKey(
        IntensiveDay, on_delete=models.CASCADE, related_name='assistants')
    priority_action = models.ForeignKey(
        PriorityAction, on_delete=models.CASCADE, related_name='assistants')
    # action = models.ForeignKey(
    # Action, on_delete=models.CASCADE, related_name='assistants')
    group = models.CharField(max_length=255)
    men = models.IntegerField(null=True, blank=True)
    women = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Asistencia de grupos de edades'
        verbose_name_plural = 'Asistencias de grupos de edades'

    def __str__(self):
        return f"Assistant {self.id}"


class FollowUp(models.Model):
    comment = models.TextField(null=True, blank=True)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name='follow_ups')
    person_count = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follow_ups_created')
    date = models.DateTimeField()

    institutions = models.ManyToManyField(
        Institution, related_name='follow_ups', blank=True)
    participants = models.ManyToManyField(
        User, related_name='follow_ups_participated', blank=True)
    agents = models.ManyToManyField(
        Agent, related_name='follow_ups', blank=True)

    class Meta:
        verbose_name = 'Seguimiento a Comunidad'
        verbose_name_plural = 'Seguimientos a Comunidades'

    def __str__(self):
        return f"Follow Up {self.id} - {self.date}"
from django.db import models


STATUS_GROUP_CHOICES = [
    ("register", "Registro"),
    ("validation", "Validación"),
    ("goal", "Objetivo"),
]
ROLE_CHOICES = [
    ("validator", "Validador"),
    ("ies", "Institución"),
]


class StatusControl(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    group = models.CharField(
        max_length=10, choices=STATUS_GROUP_CHOICES,
        verbose_name="grupo de status", default="petition")
    public_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(
        max_length=30, blank=True, null=True,
        help_text="https://vuetifyjs.com/en/styles/colors/")
    icon = models.CharField(
        max_length=40, blank=True, null=True,
        help_text="https://fonts.google.com/icons")
    order = models.IntegerField(default=4)
    is_final = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.group} - {self.public_name}"

    class Meta:
        ordering = ["group", "order"]
        verbose_name = "Status de control"
        verbose_name_plural = "Status de control (TODOS)"


class PlaceType(models.Model):
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    icon = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'place_type'

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    is_other = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'topic'

    def __str__(self):
        return self.name


class PriorityGroup(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'priority_group'

    def __str__(self):
        return self.name


class TopicGoal(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE, related_name='topics_goal')
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, related_name='topic_goals')

    class Meta:
        verbose_name = 'topic_goal'

    def __str__(self):
        return f"TopicGoal {self.id}"


class AgentType(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100)
    need_institution = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'agent_type'

    def __str__(self):
        return self.name

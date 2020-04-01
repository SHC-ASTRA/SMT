from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=64)
    discord_name = models.CharField(max_length=64, null=True, blank=True)
    # Tuples of 'code', 'readable'
    teams = ['Software', 'Electrical', 'Science', 'Mechanical', 'Other']
    team_codes = ['SW', 'EC', 'SC', 'ME', 'OT']
    team_choices = list(zip(team_codes, teams))
    team = models.CharField(max_length=2, choices=team_choices, default='OT')
    email = models.EmailField(null=True, blank=True)
    active = models.BooleanField(default=True)
    shc_member = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name) + ' (' + str(self.team) + ')'


class Subsystem(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    desc = models.TextField(
        max_length=1024, default='No description provided.')
    ac = models.TextField(max_length=2048, default='No AC provided.')
    slug = models.SlugField(default='Placeholder')
    priority = models.IntegerField(default=1)
    # If we have something over 99, we're doing it wrong
    point_value = models.DecimalField(
        default=0, max_digits=3, decimal_places=1)
    owner = models.ForeignKey(Person, models.SET_NULL, null=True, blank=True)
    parent_system = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['priority']

    @property
    def formatted_markdown(self):
        return markdownify(self.ac)

    def __str__(self):
        return str(self.slug) + ' ' + str(self.name)[:10] + '...'

    def save(self, *args, **kwargs):
        self.slug = 'SYS-' + str(self.pk).zfill(3)
        if self.parent_system:
            self.slug = 'SYS-' + \
                str(self.parent_system.pk).zfill(
                    3) + '-' + str(self.pk).zfill(3)
            self.parent_system.point_value = 0
            for subsystem in self.parent_system.subsystem_set.all():
                self.parent_system.point_value += subsystem.point_value
            self.parent_system.save()
        super().save(*args, **kwargs)


class Assignment(models.Model):
    person = models.ForeignKey(Person, models.CASCADE)
    subsystem = models.ForeignKey(Subsystem, models.CASCADE)
    team = models.CharField(max_length=2, default='ER')

    class Meta:
        ordering = ['team']
        # Prevent duplicate entries for assignments
        unique_together = ['person', 'subsystem']

    def __str__(self):
        return str(self.person) + ' -> ' + str(self.subsystem)

    def save(self, *args, **kwargs):
        if self.subsystem.parent_system:
            Upstream = type(self)(
                person=self.person, subsystem=self.subsystem.parent_system, team=self.person.team)
            try:
                Upstream.save()
            except Exception:
                pass
        self.team = self.person.team
        try:
            super().save(*args, **kwargs)
        except Exception:
            pass

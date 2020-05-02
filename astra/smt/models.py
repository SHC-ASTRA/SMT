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
    active = models.BooleanField(default=True)
    # If we have something over 99, we're doing it wrong
    point_value = models.DecimalField(
        default=0, max_digits=3, decimal_places=1)
    owner = models.ForeignKey(Person, models.SET_NULL, null=True, blank=True)
    parent_system = models.ForeignKey(
        'self', models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['priority']

    @property
    def formatted_markdown_desc(self):
        return markdownify(self.desc)

    @property
    def formatted_markdown_ac(self):
        return markdownify(self.ac)

    def __str__(self):
        return str(self.slug) + ' ' + str(self.name)[:20] + '...'

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


class PersonData(models.Model):
    team_util = models.DecimalField(
        default=0, max_digits=4, decimal_places=1, null=True, blank=True)
    avg_person_util = models.DecimalField(
        default=0, max_digits=3, decimal_places=1, null=True, blank=True)
    date = models.DateField(auto_now=True, unique=True)

    # Per dicipline stats
    sw_person_util = models.DecimalField(
        default=0, max_digits=3, decimal_places=1, null=True, blank=True)
    ec_person_util = models.DecimalField(
        default=0, max_digits=3, decimal_places=1, null=True, blank=True)
    sc_person_util = models.DecimalField(
        default=0, max_digits=3, decimal_places=1, null=True, blank=True)
    me_person_util = models.DecimalField(
        default=0, max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return 'Team Util: ' + str(self.team_util) + ' Avg Util: ' + str(self.avg_person_util) + ' - ' + str(self.date)

    def save(self, *args, **kwargs):
        # Calc team_util
        all_persons = list(Person.objects.filter(active=True))
        for assign in Assignment.objects.all():
            if assign.person in all_persons:
                all_persons.pop(all_persons.index(assign.person))
        active_team_size = len(Person.objects.filter(active=True))
        team_util = (active_team_size - len(all_persons)
                     ) / active_team_size * 100
        self.team_util = team_util

        # Calc dicipline stats
        from .person_list_utils import build_sw_team
        sw_person_util = 0
        for person in build_sw_team()['sw_people']:
            if person.assignment_set.all():
                sw_person_util += len(person.assignment_set.all())

        from .person_list_utils import build_ec_team
        ec_person_util = 0
        for person in build_ec_team()['ec_people']:
            if person.assignment_set.all():
                ec_person_util += len(person.assignment_set.all())

        from .person_list_utils import build_sc_team
        sc_person_util = 0
        for person in build_sc_team()['sc_people']:
            if person.assignment_set.all():
                sc_person_util += len(person.assignment_set.all())

        from .person_list_utils import build_me_team
        me_person_util = 0
        for person in build_me_team()['me_people']:
            if person.assignment_set.all():
                me_person_util += len(person.assignment_set.all())

        self.sw_person_util = sw_person_util / \
            len(build_sw_team()['sw_people'])
        self.ec_person_util = ec_person_util / \
            len(build_ec_team()['ec_people'])
        self.sc_person_util = sc_person_util / \
            len(build_sc_team()['sc_people'])
        self.me_person_util = me_person_util / \
            len(build_me_team()['me_people'])

        # Calc all persons avg
        self.avg_person_util = sum(
            [sw_person_util, ec_person_util, sc_person_util, me_person_util]) / active_team_size
        super().save(*args, **kwargs)


class SubsystemData(models.Model):
    active_points = models.DecimalField(
        default=0, max_digits=4, decimal_places=1, null=True, blank=True)
    date = models.DateField(unique=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return 'Active Points: ' + str(self.active_points) + ' - ' + str(self.date)

    def save(self, *args, **kwargs):
        # Calc active_points
        active_points = 0
        subsystems = Subsystem.objects.filter(parent_system=None, active=True)
        for item in subsystems:
            if item.assignment_set.all():
                active_points += item.point_value
        self.active_points = active_points
        super().save(*args, **kwargs)

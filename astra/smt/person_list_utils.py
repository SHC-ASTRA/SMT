from .models import Person


def build_sw_team():
    context = {}
    # All SW people who are active
    context['sw_people'] = Person.objects.filter(team='SW', active=True)
    # Calc number of busy vs free
    context['sw_busy'] = 0
    for person in context['sw_people']:
        if len(person.assignment_set.all()) != 0:
            context['sw_busy'] += 1
    context['sw_free'] = len(context['sw_people']) - context['sw_busy']
    return context


def build_ec_team():
    context = {}
    # All EC people who are active
    context['ec_people'] = Person.objects.filter(team='EC', active=True)
    # Calc number of busy vs free
    context['ec_busy'] = 0
    for person in context['ec_people']:
        if len(person.assignment_set.all()) != 0:
            context['ec_busy'] += 1
    context['ec_free'] = len(context['ec_people']) - context['ec_busy']
    return context


def build_sc_team():
    context = {}
    # All SC people who are active
    context['sc_people'] = Person.objects.filter(team='SC', active=True)
    # Calc number of busy vs free
    context['sc_busy'] = 0
    for person in context['sc_people']:
        if len(person.assignment_set.all()) != 0:
            context['sc_busy'] += 1
    context['sc_free'] = len(context['sc_people']) - context['sc_busy']
    return context


def build_me_team():
    context = {}
    # All ME people who are active
    context['me_people'] = Person.objects.filter(team='ME', active=True)
    # Calc number of busy vs free
    context['me_busy'] = 0
    for person in context['me_people']:
        if len(person.assignment_set.all()) != 0:
            context['me_busy'] += 1
    context['me_free'] = len(context['me_people']) - context['me_busy']
    return context

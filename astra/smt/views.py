from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


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


def build_subsystems():
    context = {}
    # Add all top-level subsystems
    context['subsystems'] = Subsystem.objects.filter(parent_system=None)
    return context


def index(request):
    context = {}
    context['all_subsystems'] = Subsystem.objects.all()
    context.update(build_sw_team())
    context.update(build_ec_team())
    context.update(build_sc_team())
    context.update(build_me_team())
    context.update(build_subsystems())
    return render(request, 'smt/head.html', context=context)


@csrf_exempt
def add_person_to_subsystem(request):
    if request.method != 'POST':
        messages.warning(
            request, 'You attempted to GET a POST (add_person_to_subsystem)')
        return redirect('/')
    error = False
    if 'person_pk' not in request.POST:
        error = True
        messages.warning(
            request, 'No value for person supplied (add_person_to_subsystem)')
    if 'sys_pk' not in request.POST:
        error = True
        messages.warning(
            request, 'No value for subsystem supplied (add_person_to_subsystem)')
    if error:
        return redirect('/')
    # Yes, i'm using single letter variables. @me
    p = Person.objects.get(pk=request.POST['person_pk'])
    s = Subsystem.objects.get(pk=request.POST['sys_pk'])
    Task = Assignment(person=p, subsystem=s)
    Task.save()
    return HttpResponse('OK')


@csrf_exempt
def remove_assignment(request):
    if request.method != 'POST':
        messages.warning(
            request, 'You attempted to GET a POST (remove_assignment)')
        return redirect('/')
    if 'assign_pk' not in request.POST:
        messages.warning(
            request, 'Assignment not found (remove_assignment)')
        return redirect('/')
    a = Assignment.objects.get(pk=request.POST['assign_pk'])
    a.delete()
    return HttpResponse('OK')


def create_subsystem(request):
    if request.method != 'POST':
        messages.warning(
            request, 'You attempted to GET a POST (create_subsystem)')
    try:
        # First form group
        name = request.POST['name']
        desc = request.POST['desc']
        ac = request.POST['ac']
        # Second form group
        priority = request.POST['priority']
        pv = request.POST['point_value']
        # Third form group
        if request.POST['parent_system'] is 'None':
            parent = None
        else:
            parent = Subsystem.objects.get(pk=request.POST['parent_system'])
        # Initialize subsystem with those values and save
        s = Subsystem(name=name, desc=desc, ac=ac, priority=priority,
                      point_value=pv, parent_system=parent)
        s.save()
        s.save()
    except Exception as e:
        messages.warning(request, 'Something went wrong (create_subsystem)!')
        messages.warning(request, str(e))
    return redirect('/')


def failed_to_contact(request):
    if 'person' not in request.GET:
        messages.warning(
            request, 'There is no contact information for this person.')
    else:
        messages.warning(
            request, 'There is no contact information for ' + request.GET['person'] + '.')
    return redirect('/')

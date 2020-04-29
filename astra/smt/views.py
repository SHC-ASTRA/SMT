from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .person_list_utils import *
from .models import *


def build_subsystems():
    context = {}
    # Add all top-level subsystems
    context['subsystems'] = Subsystem.objects.filter(
        parent_system=None, active=True)
    return context


def build_person_data():
    context = {}
    context['latest_person_data'] = PersonData.objects.all()[0]
    context['person_data_hist'] = list(
        PersonData.objects.all())[-10:]
    return context


def index(request):
    context = {}
    context['all_subsystems'] = Subsystem.objects.filter(active=True)
    context.update(build_sw_team())
    context.update(build_ec_team())
    context.update(build_sc_team())
    context.update(build_me_team())
    context.update(build_subsystems())
    context.update(build_person_data())
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
        if request.POST['parent_system'] == '':
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


def edit_subsystem(request):
    if request.method != 'POST':
        messages.warning(
            request, 'You attempted to GET a POST (create_subsystem)')
    try:
        # First form group
        pk = request.POST['pk']
        name = request.POST['name']
        desc = request.POST['desc']
        ac = request.POST['ac']
        # Second form group
        priority = request.POST['priority']
        pv = request.POST['point_value']
        # Third form group
        if request.POST['parent_system'] == '':
            parent = None
        else:
            parent = Subsystem.objects.get(pk=request.POST['parent_system'])
        # Initialize subsystem with those values and save
        s = Subsystem.objects.get(pk=pk)
        s.name = name
        s.desc = desc
        s.ac = ac
        s.priority = priority
        s.point_value = pv
        s.parent_system = parent
        s.save()
    except Exception as e:
        messages.warning(request, 'Something went wrong (edit_subsystem)!')
        messages.warning(request, str(e))
    return redirect('/')


def archive_subsystem(request):
    # Should really be a post request but this is easier
    if not request.user.is_authenticated:
        messages.warning(
            request, 'You do not have permission (archive_subsystem)')
        return redirect('/')
    if 'pk' not in request.GET:
        messages.warning(
            request, 'Something went wrong (archive_subsystem)!')
        return redirect('/')
    try:
        s = Subsystem.objects.get(pk=request.GET['pk'])
        s.active = False
        s.save()
    except Exception as e:
        messages.warning(request, 'Something went wrong (edit_subsystem)!')
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

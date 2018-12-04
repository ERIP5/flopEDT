# -*- coding: utf-8 -*-

# This file is part of the FlOpEDT/FlOpScheduler project.
# Copyright (c) 2017
# Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.
# 
# You can be released from the requirements of the license by purchasing
# a commercial license. Buying such a license is mandatory as soon as
# you develop activities involving the FlOpEDT/FlOpScheduler software
# without disclosing the source code of your own applications.

import json
from collections import namedtuple
from itertools import chain
from random import randint
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, Http404, JsonResponse, HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView

from people.models import Tutor

from base.admin import CoursResource, DispoResource, VersionResource, \
    CoursPlaceResource, BreakingNewsResource, UnavailableRoomsResource
from base.forms import ContactForm
from base.models import Course, UserPreference, ScheduledCourse, EdtVersion, \
    CourseModification, Slot, Day, Time, RoomGroup, PlanningModification, \
    Regen, BreakingNews, RoomPreference, Department, TimeGeneralSettings
import base.queries as queries
from base.weeks import *


logger = logging.getLogger(__name__)

# <editor-fold desc="FAVICON">
# ----------
# FAVICON
# ----------


fav_regexp = r'^(?P<fav>(favicon.ico)|(site\.webmanifest)' \
             r'|(browserconfig\.xml)|(safari-pinned-tab.svg)' \
             r'|(mstile.*\.png)|(favicon.*\.png)|(android-chrome.*\.png)' \
             r'|(apple-touch-icon.*\.png))$'


def favicon(req, fav, **kwargs):
    return RedirectView.as_view(
        url=staticfiles_storage.url('base/img/favicons/' + fav),
        permanent=False)(req)


# </editor-fold desc="FAVICON">


# <editor-fold desc="VIEWERS">
# ----------
# VIEWERS
# ----------
def index(req):
    """
    Display department selection view.
    
    The view create a default department if not exist and 
    redirects to edt vue if only one department exist
    """
    def redirect_to_edt(department):
        reverse_url = reverse('base:edt', kwargs={'department': department.abbrev})
        #reverse_url = reverse('base:edt', department=department.abbrev)
        return reverse_url

    departments = Department.objects.all()

    if not departments:        
        # Create first department
        department = queries.create_first_department()
        return redirect(redirect_to_edt(department))
    elif len(departments) == 1:
        return redirect(redirect_to_edt(departments[0]))
    else:
        return TemplateResponse(req, 'base/departments.html', {'departments': departments})

def edt(req, an=None, semaine=None, splash_id=0, **kwargs):

    semaine, an = clean_edt_view_params(semaine, an)
    promo = clean_train_prog(req)

    if req.GET:
        copie = req.GET.get('cop', '0')
        copie = int(copie)
        gp = req.GET.get('gp', '')
    else:
        copie = 0
        gp = ''

    # une_salle = RoomGroup.objects.all()[1].name
    une_salle = 'salle?'

    if req.user.is_authenticated:
        name_usr = req.user.username
        try:
            rights_usr = req.user.rights
        except ObjectDoesNotExist:
            rights_usr = 0
    else:
        name_usr = ''
        rights_usr = 0

    return TemplateResponse(req, 'base/show-edt.html',
            {
                'all_weeks': week_list(),
                'semaine': semaine,
                'an': an,
                'promo': promo,
                'une_salle': une_salle,
                'copie': copie,
                'gp': gp,
                'name_usr': name_usr,
                'rights_usr': rights_usr,
                'splash_id': splash_id,
                'time_settings': queries.get_time_settings(req.department),
                'days': num_all_days(an, semaine, req.department)
            })


def edt_light(req, an=None, semaine=None, **kwargs):
    semaine, an = clean_edt_view_params(semaine, an)
    promo = clean_train_prog(req)

    if req.GET:
        svg_h = req.GET.get('svg_h', '640')
        svg_w = req.GET.get('svg_w', '1370')
        gp_h = req.GET.get('gp_h', '40')
        gp_w = req.GET.get('gp_w', '30')
        svg_top_m = req.GET.get('top_m', '40')

        svg_h = int(svg_h)
        svg_w = int(svg_w)
        gp_h = int(gp_h)
        gp_w = int(gp_w)
        svg_top_m = int(svg_top_m)

    else:
        svg_h = 640
        svg_w = 1370
        gp_h = 40
        gp_w = 30
        svg_top_m = 40

    une_salle = "salle?"  # RoomGroup.objects.all()[0].name

    return TemplateResponse(req, 'base/show-edt-light.html',
                  {'all_weeks': week_list(),
                   'semaine': semaine,
                   'an': an,
                   'une_salle': une_salle,
                   'tv_svg_h': svg_h,
                   'tv_svg_w': svg_w,
                   'tv_gp_h': gp_h,
                   'tv_gp_w': gp_w,
                   'promo': promo,
                   'tv_svg_top_m': svg_top_m
                  })


@login_required
def stype(req, **kwargs):
    err = ''
    if req.method == 'GET':
        return TemplateResponse(req,
                      'base/show-stype.html',
                      {'date_deb': current_week(),
                       'date_fin': current_week(),
                       'name_usr': req.user.username,
                       'err': err,
                       'annee_courante': annee_courante
                      })
    elif req.method == 'POST':
        if 'apply' in list(req.POST.keys()):
            print(req.POST['se_deb'])
            date_deb = {'semaine': req.POST['se_deb'],
                        'an': req.POST['an_deb']}
            date_fin = {'semaine': req.POST['se_fin'],
                        'an': req.POST['an_fin']}
            if date_deb['an'] < date_fin['an'] or \
                    (date_deb['an'] == date_fin['an']
                     and date_deb['semaine'] <= date_fin['semaine']):
                print(req.POST['apply'])
            else:
                date_deb = current_week()
                date_fin = current_week()
                err = "Problème : seconde semaine avant la première"

        else:
            date_deb = current_week()
            date_fin = current_week()

            print(req.POST['save'])

        return TemplateResponse(req,
                      'base/show-stype.html',
                      {'date_deb': date_deb,
                       'date_fin': date_fin,
                       'name_usr': req.user.username,
                       'err': err,
                       'annee_courante': annee_courante
                      })


def aide(req, **kwargs):
    return TemplateResponse(req, 'base/aide.html')


@login_required
def decale(req, **kwargs):
    if req.method != 'GET':
        return TemplateResponse(req, 'base/aide.html', {})

    semaine_init = req.GET.get('s', '-1')
    an_init = req.GET.get('a', '-1')
    department = req.department

    liste_profs = []

    for p in Tutor.objects \
                    .filter(departments=department) \
                    .order_by('username'):
        liste_profs.append(p.username)

    return TemplateResponse(req, 'base/show-decale.html',
                  {'all_weeks': week_list(),
                   'semaine_init': semaine_init,
                   'an_init': an_init,
                   'profs': liste_profs
                  })


# </editor-fold desc="VIEWERS">


# <editor-fold desc="FETCHERS">
# ----------
# FETCHERS
# ----------


def fetch_cours_pl(req, year, week, num_copy, **kwargs):
    logger.info(f'REQ: fetch sched courses: {req}')

    try:
        week = int(week)
        year = int(year)
        num_copy = int(num_copy)
        department = req.department
    except:
        return HttpResponse("KO")

    logger.info(f"D{department} W{week} Y{year} N{num_copy}")

    cache_key = get_key_course_pl(department.abbrev, year, week, num_copy)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    ok = False
    version = 0
    dataset = None
    while not ok:
        if num_copy == 0:
            version = queries.get_edt_version(department=department,
                    week=week,
                    year=year, create=True)
        
        dataset = CoursPlaceResource() \
            .export(queries.get_scheduled_courses(
                        department=department,                         
                        week=week,
                        year=year,
                        num_copy=num_copy)
            )
        ok = num_copy != 0 \
             or (version == queries \
                                .get_edt_version(
                                    department=department, 
                                    week=week, 
                                    year=year))

    if dataset is None:
        raise Http404("What are you trying to do?")

    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['version'] = version
    response['week'] = week
    response['year'] = year
    response['num_copy'] = num_copy
    
    try:
        regen = str(Regen.objects.get(department=department, semaine=week, an=year))
    except ObjectDoesNotExist:
        regen = 'I'
    response['regen'] = regen

    if req.user.is_authenticated:
        response['reqDispos'] = Course \
                                    .objects \
                                    .filter(tutor=req.user,
                                            semaine=week,
                                            an=year) \
                                    .count() * 2
        week_av = UserPreference \
            .objects \
            .filter(user=req.user,
                    semaine=week,
                    an=year)
        if not week_av.exists():
            response['filDispos'] = UserPreference \
                .objects \
                .filter(user=req.user,
                        semaine=None,
                        valeur__gte=1) \
                .count()
        else:
            response['filDispos'] = week_av \
                .filter(valeur__gte=1) \
                .count()
    else:
        response['reqDispos'] = -1
        response['filDispos'] = -1

    cached = cache.set(cache_key, response)
    return response


def fetch_cours_pp(req, week, year, num_copy, **kwargs):
    logger.info(f"REQ: unscheduled courses; {req}")

    try:
        week = int(week)
        year = int(year)
        num_copy = int(num_copy)
        department = req.department
    except ValueError:
        return HttpResponse("KO")

    logger.info(f"D{department} W{week} Y{year} N{num_copy}")

    cache_key = get_key_course_pp(department.abbrev, year, week, num_copy)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    dataset = CoursResource() \
        .export(Course
                .objects
                .filter(
                        module__train_prog__department=department,
                        semaine=week,
                        an=year)
                .exclude(pk__in=ScheduledCourse
                         .objects
                         .filter(
                             cours__module__train_prog__department=department,
                             copie_travail=num_copy)
                         .values('cours')))
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['week'] = week
    response['year'] = year

    cache.set(cache_key, response)
    return response


#@login_required
def fetch_dispos(req, year, week, **kwargs):
    logger.info(f"REQ: fetch dispos; {req}")
    if req.GET:
        if not req.user.is_authenticated:
            return HttpResponse("Pas connecte")

    try:
        week = int(week)
        year = int(year)
        department = req.department
    except ValueError:
        return HttpResponse("KO")

    cache_key = get_key_preferences_tutor(department.abbrev, year, week)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    busy_inst = Course.objects.filter(semaine=week,
                                      an=year,
                                      module__train_prog__department=department) \
        .distinct('tutor') \
        .values_list('tutor')

    busy_inst = list(chain(busy_inst, [req.user]))

    week_avail = UserPreference.objects \
        .filter(semaine=week,
                an=year,
                user__in=busy_inst) \

    default_avail = UserPreference.objects \
        .exclude(user__in \
                     =week_avail \
                 .distinct('user') \
                 .values_list('user')) \
        .filter(semaine=None,
                user__in=busy_inst) \

    dataset = DispoResource() \
        .export(list(chain(week_avail,
                           default_avail)))  # all())#
    response = HttpResponse(dataset.csv,
                            content_type='text/csv')
    response['week'] = week
    response['year'] = year

    cache.set(cache_key, response)
    return response
    #     else:
    #         return HttpResponse("Pas connecté", status=500)
    # else:
    #     return HttpResponse("Pas GET", status=500)


def fetch_unavailable_rooms(req, year, week, **kwargs):
    print(req)
    print("================")
    # if req.GET:
    #     if req.user.is_authenticated:
    print("================")


    try:
        week = int(week)
        year = int(year)
        department = req.department
    except ValueError:
        return HttpResponse("KO")

    # ----------------
    # To be done later
    # ----------------
    #
    # cache_key = get_key_unavailable_rooms(department.abbrev, year, week)
    # cached = cache.get(cache_key)
    # if cached is not None:
    #     return cached

    # dataset = DispoResource() \
    #     .export(RoomPreference.objects.filter(
    #                                         room__departments = department, 
    #                                         semaine=week,
    #                                         an=year,
    #                                         valeur=0))
    # response = HttpResponse(dataset.csv,
    #                         content_type='text/csv')
    # cache.set(cache_key, response)


    response = HttpResponse(content_type='text/csv')
    response['week'] = week
    response['year'] = year

    return response
   

def fetch_all_tutors(req, **kwargs):
    cache_key = get_key_all_tutors()
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    tutor_list = [t.username for t in Tutor.objects.all()]
    response = JsonResponse({'tutors': tutor_list})
    cache.set(cache_key, response)
    return response


@login_required
def fetch_stype(req, **kwargs):
    # if req.method == 'GET':
    dataset = DispoResource() \
        .export(UserPreference.objects \
                .filter(semaine=None,
                        user=req.user))  # all())#
    response = HttpResponse(dataset.csv, content_type='text/csv')
    return response
    # else:
    #    return HttpResponse("Pas GET",status=500)


def fetch_decale(req, **kwargs):
    if not req.is_ajax() or req.method != "GET":
        return HttpResponse("KO")

    semaine = int(req.GET.get('s', '0'))
    an = int(req.GET.get('a', '0'))
    module = req.GET.get('m', '')
    prof = req.GET.get('p', '')
    groupe = req.GET.get('g', '')
    department = req.department

    courses = []
    modules = []
    tutors = []
    module_tutors = []
    groups = []

    if an > 0 and semaine > 0:
        days = num_all_days(an, semaine, req.department)
    else:
        days = []

    cours = filt_p(filt_g(filt_m(filt_sa(department, semaine, an), module), groupe), prof)

    for c in cours:
        try:
            cp = ScheduledCourse.objects.get(cours=c,
                                             copie_travail=0)
            day = cp.day
            time = cp.start_time
        except ObjectDoesNotExist:
            day = ''
            time = -1
        if c.tutor is not None:
            courses.append({'i': c.id,
                            'm': c.module.abbrev,
                            'p': c.tutor.username,
                            'g': c.groupe.nom,
                            'd': day,
                            't': time})

    cours = filt_p(filt_g(filt_sa(department, semaine, an), groupe), prof) \
        .order_by('module__abbrev') \
        .distinct('module__abbrev')
    for c in cours:
        modules.append(c.module.abbrev)

    cours = filt_g(filt_m(filt_sa(department, semaine, an), module), groupe) \
        .order_by('tutor__username') \
        .distinct('tutor__username')
    for c in cours:
        if c.tutor is not None:
            tutors.append(c.tutor.username)

    if module != '':
        cours_queryset = Course.objects.filter(module__train_prog__department=department)        
        cours = filt_m(cours_queryset, module) \
            .order_by('tutor__username') \
            .distinct('tutor__username')
        for c in cours:
            if c.tutor is not None:
                module_tutors.append(c.tutor.username)

    cours = filt_p(filt_m(filt_sa(department, semaine, an), module), prof) \
        .distinct('groupe')
    for c in cours:
        groups.append(c.groupe.nom)

    return JsonResponse({'cours': courses,
                         'modules': modules,
                         'profs': tutors,
                         'profs_module': module_tutors,
                         'groupes': groups,
                         'jours': days})


def fetch_bknews(req, year, week, **kwargs):
    dataset = BreakingNewsResource() \
        .export(BreakingNews.objects.filter(
                                        department=req.department,
                                        year=year,
                                        week=week))
    response = HttpResponse(dataset.csv,
                            content_type='text/csv')
    response['semaine'] = week
    response['an'] = year
    return response


def fetch_all_versions(req, **kwargs):

    dataset = VersionResource() \
        .export(EdtVersion.objects.filter(department=req.department))
    response = HttpResponse(dataset.json,
                            content_type='text/json')
    return response


@cache_page(15 * 60)
def fetch_groups(req, **kwargs):
    """
    Return groups tree for a given department
    """
    groups = queries.get_groups(req.department.abbrev)
    return JsonResponse(groups, safe=False)

#@cache_page(15 * 60)
def fetch_rooms(req, **kwargs):
    """
    Return rooms for a given department
    """
    rooms = queries.get_rooms(req.department.abbrev)
    return JsonResponse(rooms, safe=False)    

def fetch_constraints(req, **kwargs):
    """
    Return course type constraints for a given department
    """
    constraints = queries.get_coursetype_constraints(req.department.abbrev)
    return JsonResponse(constraints, safe=False)    

# </editor-fold desc="FETCHERS">

# <editor-fold desc="CHANGERS">
# ----------
# CHANGERS
# ----------


@login_required
def edt_changes(req, **kwargs):
    bad_response = HttpResponse("KO")
    good_response = HttpResponse("OK")

    if not req.user.is_tutor:
        bad_response['reason'] = "Pas membre de l'équipe encadrante"
        return bad_response
        

    impacted_inst = set()

    msg = 'Notation : (numero_semaine, numero_annee, ' \
          + 'numero_jour, numero_creneau, prof)\n\n'

    if not req.is_ajax():
        bad_response['reason'] = "Non ajax"
        return bad_response

    if req.method != "POST":
        bad_response['reason'] = "Non POST"
        return bad_response


    try:
        semaine = req.GET.get('s', '')
        an = req.GET.get('a', '')
        work_copy = req.GET.get('c', '')
        semaine = int(semaine)
        an = int(an)
        work_copy = int(work_copy)
        version = None
        department = req.department
    except:
        bad_response['reason'] \
            = "Problème semaine, année ou work_copy."
        return bad_response


    logger.info(f"REQ: edt change; {req.body}")
    logger.info(req.POST)
    old_version = json.loads(req.POST.get('v',-1))
    recv_changes = json.loads(req.POST.get('tab',[]))


    if work_copy == 0:
        version = queries.get_edt_version(department, semaine, an, create=True)

    if work_copy != 0 or old_version == version:
        with transaction.atomic():
            if work_copy == 0:
                edt_version = EdtVersion \
                    .objects \
                    .select_for_update() \
                    .get(department=department, semaine=semaine, an=an)
            for a in recv_changes:
                non_place = False
                co = Course.objects.get(id=a['id'])
                try:
                    cp = ScheduledCourse.objects.get(cours=co,
                                                     copie_travail=work_copy)
                except ObjectDoesNotExist:
                    non_place = True
                    cp = ScheduledCourse(cours=co,
                                         copie_travail=work_copy)

                m = CourseModification(cours=co,
                                       version_old=old_version,
                                       initiator=req.user.tutor)
                # old_day = a.day.o
                # old_slot = a.slot.o
                new_day = a['day']['n']
                old_day = a['day']['o']
                new_start_time = a['start']['n']
                old_start_time = a['start']['o']
                old_room = a['room']['o']
                new_room = a['room']['n']
                new_week = a['week']['n']
                old_week = a['week']['o']
                new_year = a['year']['n']
                old_year = a['year']['o']
                new_tutor = a['tutor']['n']
                old_tutor = a['tutor']['o']

                if non_place:
                    # old_day = new_day
                    # old_slot = new_slot
                    if new_room is None:
                        new_room = old_room

                if new_day is not None:
                    # None, None means no change
                    # same, same means not scheduled before
                    if non_place:
                        cp.day = new_day
                        cp.start_time = new_start_time
                    m.day_old = cp.day
                    m.start_time_old = cp.start_time
                    cp.day = new_day
                    cp.start_time = new_start_time
                    logger.info(f"Course modification: {m}")
                    logger.info(f"New scheduled course: {cp}")
                if new_room is not None:
                    try:
                        sal_n = RoomGroup.objects.get(name=new_room)
                    except ObjectDoesNotExist:
                        if new_room == 'salle?':
                            bad_response['reason'] \
                                = 'Oublié de trouver une salle ' \
                                  'pour un cours ?'
                        else:
                            bad_response['reason'] = \
                                f"Problème : salle {new_room} inconnue"
                        return bad_response

                    if non_place:
                        cp.room = sal_n
                    m.room_old = cp.room
                    cp.room = sal_n
                if new_week is not None:
                    m.semaine_old = old_week
                    m.an_old = old_year
                    cp.cours.semaine = new_week
                    cp.cours.an = new_year
                cp.save()
                if work_copy == 0:
                    m.save()

                if new_tutor is not None:
                    try:
                        prev_tut = co.tutor
                        co.tutor = Tutor.objects.get(username=new_tutor)
                        co.save()
                        pm = PlanningModification(cours=co,
                                                  semaine_old=co.semaine,
                                                  an_old=co.an,
                                                  tutor_old=prev_tut,
                                                  initiator=req.user.tutor)
                        pm.save()
                    except ObjectDoesNotExist:
                        bad_response['reason'] = \
                            f"Problème : prof {new_tutor} inconnu"
                        return bad_response

                if new_week is not None or new_year is not None \
                   or new_day is not None or new_start_time is not None \
                   or new_tutor is not None:
                    msg += str(co) + '\n'
                    impacted_inst.add(co.tutor.username)
                    if new_tutor is not None:
                        impacted_inst.add(old_tutor)

                    msg += f'({old_week}, {old_year}, ' \
                           + f'{old_day}, {old_start_time}, {old_tutor})'
                    msg += ' -> ('
                    msg += str(new_week) if new_week is not None else '-'
                    msg += ', '
                    msg += str(new_year) if new_year is not None else '-'
                    msg += ', '
                    msg += str(new_day) if new_day is not None else '-'
                    msg += ', '
                    msg += str(new_start_time) if new_start_time is not None else '-'
                    msg += ','
                    msg += str(new_tutor) if new_tutor is not None else '-'
                    msg += ')\n\n'

            if work_copy == 0:
                edt_version.version += 1
                edt_version.save()

            if new_week is not None and new_year is not None:
                cache.delete(get_key_course_pl(department.abbrev, new_year, new_week, work_copy))
            cache.delete(get_key_course_pl(department.abbrev, old_year, old_week, work_copy))
            cache.delete(get_key_course_pp(department.abbrev, old_year, old_week, work_copy))
            

        # subject = '[Modif sur tierce] ' + req.user.username \
        #           + ' a déplacé '
        # for inst in impacted_inst:
        #     if inst is not req.user.username:
        #         subject += inst + ' '

        # if len(impacted_inst) > 0 and work_copy == 0:
        #     if len(impacted_inst) > 1 \
        #             or req.user.username not in impacted_inst:
        #         send_mail(
        #             subject,
        #             msg,
        #             'edt@iut-blagnac',
        #             ['edt.info.iut.blagnac@gmail.com']
        #         )
        logger.info('Envoi de mail')
        logger.info(msg)
        

        return good_response
    else:
        bad_response['reason'] = f"Version: {version} VS {old_version}"
        return bad_response


@login_required
def dispos_changes(req, **kwargs):
    bad_response = HttpResponse("KO")
    good_response = HttpResponse("OK")

    if not req.is_ajax():
        bad_response['reason'] = "Non ajax"
        return bad_response

    if req.method != "POST":
        bad_response['reason'] = "Non POST"
        return bad_response


    try:
        week = req.GET.get('s', '')
        year = req.GET.get('a', '')
        week = int(week)
        year = int(year)
    except ValueError:
        bad_response['reason'] \
            = "Problème semaine ou année."
        return bad_response

    usr_change = req.GET.get('u', '')
    if usr_change == '':
        usr_change = req.user.username

    # Default week at None
    if week == 0 or year == 0:
        week = None
        year = None

    logger.info(f"REQ: dispo change; {req.body}")
    logger.info(req.POST)
    # q = json.loads(req.body,
    #                object_hook=lambda d:
    #                namedtuple('X', list(d.keys()))(*list(d.values())))
    q = json.loads(req.POST.get('changes','{}'))
    logger.info("List of changes")
    for a in q:
        logger.info(a)

    
    prof = None
    try:
        prof = Tutor.objects.get(username=usr_change)
    except ObjectDoesNotExist:
        bad_response['reason'] \
            = "Problème d'utilisateur."
        return bad_response

    if prof.username != req.user.username and req.user.rights >> 1 % 2 == 0:
        bad_response['reason'] \
            = 'Non autorisé, réclamez plus de droits.'
        return bad_response

    # print(q)

    # if no preference was present for this week, first copy the
    # default availabilities

    if not UserPreference.objects.filter(user=prof,
                                         semaine=week,
                                         an=year).exists():
        for pref in UserPreference.objects.filter(user=prof,
                                                  semaine=None):
            new_dispo = UserPreference(user=prof,
                                       semaine=week,
                                       an=year,
                                       day=pref.day,
                                       start_time=pref.start_time,
                                       duration=pref.duration,
                                       valeur=pref.valeur)
            logger.info(new_dispo)
            new_dispo.save()

    for a in q:
        logger.info(f"Change {a}")
        UserPreference.objects.filter(user=prof,
                                      semaine=week,
                                      an=year,
                                      day=a['day']).delete()
        for pref in a['val_inter']:
            new_dispo = UserPreference(user=prof,
                                       semaine=week,
                                       an=year,
                                       day=a['day'],
                                       start_time=pref['start_time'],
                                       duration=pref['duration'],
                                       valeur=pref['value'])
            logger.info(new_dispo)
            new_dispo.save()
            
        # cr = Slot.objects \
        #     .get(jour=Day.objects.get(no=a['day']),
        #          heure=Time.objects.get(no=a['hour']))
        # if cr is None:
        #     bad_response['reason'] = "Creneau pas trouve"
        #     return bad_response
        # di, didi = UserPreference \
        #     .objects \
        #     .update_or_create(user=prof,
        #                       semaine=week,
        #                       an=year,
        #                       creneau=cr,
        #                       defaults={'valeur': a['val']})
        # logger.info("  Update or create")
        # logger.info(f"  {di}")
        # logger.info(f"  {didi}")
        
    if week is not None and year is not None:
        for c in Course.objects.filter(semaine=week,
                                       an=year).distinct('module__train_prog__department'):
            cache.delete(get_key_preferences_tutor(c.module.train_prog.department.abbrev,
                                                   year, week))
        
    return good_response


@login_required
def decale_changes(req, **kwargs):
    bad_response = HttpResponse("KO")
    good_response = HttpResponse("OK")
    print(req)

    if not req.is_ajax():
        bad_response['reason'] = "Non ajax"
        return bad_response

    if req.method != "POST":
        bad_response['reason'] = "Non POST"
        return bad_response

    new_assignment = json.loads(req.POST.get('new',{}))
    change_list = json.loads(req.POST.get('liste',[]))

    for c in change_list:
        # try:
        if c['d'] != '' and c['t'] != -1:
            cours_place = ScheduledCourse \
                .objects \
                .get(cours__id=c['i'],
                     copie_travail=0)
            cours = cours_place.cours
            cache.delete(get_key_course_pl(req.department.abbrev,
                                           cours.an,
                                           cours.semaine,
                                           cours_place.copie_travail))
            cours_place.delete()
        else:
            cours = Course.objects.get(id=c['i'])
            cache.delete(get_key_course_pp(req.department.abbrev, 
                                           cours.an,
                                           cours.semaine,
                                           0))
            # note: add copie_travail in Cours might be of interest

        pm = PlanningModification(cours=cours,
                                  semaine_old=cours.semaine,
                                  an_old=cours.an,
                                  tutor_old=cours.tutor,
                                  initiator=req.user.tutor)
        pm.save()

        cours.semaine = new_assignment['ns']
        cours.an = new_assignment['na']
        if new_assignment['na'] != 0:
            # cours.prof=User.objects.get(username=a.np)
            cours.tutor = Tutor.objects.get(username=new_assignment['np'])
        cache.delete(get_key_course_pp(req.department.abbrev,
                                       cours.an,
                                       cours.semaine,
                                       0))
        cours.save()


    return good_response


# </editor-fold desc="CHANGERS">

# <editor-fold desc="EMAILS">
# ---------
# E-MAILS
# ---------


def contact(req, **kwargs):
    ack = ''
    if req.method == 'POST':
        form = ContactForm(req.POST)
        if form.is_valid():
            dat = form.cleaned_data
            recip_send = [Tutor.objects.get(username=
                                            dat.get("recipient")).email,
                          dat.get("sender")]
            try:
                send_mail(
                    '[EdT IUT Blagnac] ' + dat.get("subject"),
                    "(Cet e-mail vous a été envoyé depuis le site des emplois"
                    " du temps de l'IUT de Blagnac)\n\n"
                    + dat.get("message"),
                    dat.get("sender"),
                    recip_send,
                )
            except:
                ack = 'Envoi du mail impossible !'
                return TemplateResponse(req, 'base/contact.html',
                              {'form': form,
                               'ack': ack
                              })

            return edt(req, None, None, 1)
    else:
        init_mail = ''
        if req.user.is_authenticated:
            init_mail = req.user.email
        form = ContactForm(initial={
            'sender': init_mail})
    return TemplateResponse(req, 'base/contact.html',
                  {'form': form,
                   'ack': ack
                  })


# </editor-fold desc="EMAILS">

# <editor-fold desc="HELPERS">
# ---------
# HELPERS
# ---------


def clean_train_prog(req):
    if req.GET:
        promo = req.GET.get('promo', '0')
        try:
            promo = int(promo)
        except ValueError:
            promo = 0
        if promo not in [1, 2, 3]:
            promo = 0
    else:
        promo = 0
    return promo


def clean_edt_view_params(week, year):

    if week is None or year is None:
        today = current_week()
        week = today['semaine']
        year = today['an']
    else:
        try:
            week = int(week)
            year = int(year)
        except ValueError:
            today = current_week()
            week = today['semaine']
            year = today['an']

    return week, year


def filt_m(r, module):
    if module != '':
        r = r.filter(module__abbrev=module)
    return r


def filt_p(r, prof):
    if prof != '':
        r = r.filter(tutor__username=prof)
    return r


def filt_g(r, groupe):
    if groupe != '':
        r = r.filter(groupe__nom=groupe)
    return r


def filt_sa(department, semaine, an):
    return Course.objects.filter(module__train_prog__department=department,
                                 semaine=semaine,
                                 an=an)


def get_key_course_pl(department_abbrev, year, week, num_copy):
    if year is None or week is None or num_copy is None:
        return ''
    return 'CPL-D' + department_abbrev + '-Y' + str(year) + '-W' + str(week) + '-C' + str(num_copy) 


def get_key_course_pp(department_abbrev, year, week, num_copy):
    if year is None or week is None or num_copy is None:
        return ''
    return 'CPP-D' + department_abbrev + '-Y' + str(year) + '-W' + str(week) + '-C' + str(num_copy) 


def get_key_preferences_tutor(department_abbrev, year, week):
    if year is None or week is None:
        return ''
    return 'PREFT-D' + department_abbrev + '-Y' + str(year) + '-W' + str(week)


def get_key_unavailable_rooms(department_abbrev, year, week):
    if year is None or week is None:
        return ''
    return 'UNAVR-D' + department_abbrev + '-Y' + str(year) + '-W' + str(week)


def get_key_all_tutors():
    return 'ALL-TUT'

# </editor-fold desc="HELPERS">




from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Week, Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_scheduled_course import week1, week7, module_algo_prog, module_conception_log, training_l3_miashs ,training_l2_miashs, \
department_miashs, period_1 , period_2, tutor_algo_prog, tutor_conception, \
course_type_algo, room_algo, course_algo, scheduled1, \
course_type_conception, room_conception, course_conception, scheduled2
from lib import *

@pytest.fixture
def department_info(db) -> Department:
    return Department.objects.create(abbrev="INFO", name="informatique")

@pytest.fixture
def department_reseaux(db) -> Department:
    return Department.objects.create(abbrev="RT", name="reseaux et telecommunication")

@pytest.fixture
def tutor_info(db, department_info : Department) -> Tutor:
    res = Tutor.objects.create(username="LN",  first_name="Laurent")
    res.save()
    res.departments.add(department_info)
    res.save()
    return res

@pytest.fixture
def tutor_reseaux(db, department_reseaux : Department) -> Tutor:
    res = Tutor.objects.create(username="ADES",  first_name="Arnaud")
    res.save()
    res.departments.add(department_reseaux)
    res.save()
    return res

def test_all_tutors_dept(client_query,
                    tutor_info : Tutor, 
                    tutor_reseaux : Tutor):
    query='''
        query {
            tutors (dept : \"RT\") {
                edges {
                    node {
                        username
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "tutors")
    data = get_data(res)
    assert tutor_reseaux.username in data["username"]
    assert tutor_info.username not in data["username"]

def test_tutors_algo(client_query,
                           tutor_algo_prog: Tutor, scheduled1 : ScheduledCourse, scheduled2 : ScheduledCourse):
    query='''
        query {
            tutors (dept : \"MIASHS\", week : 7, year : 2021){
                edges {
                    node {
                        username
                        firstName
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "tutors")
    data = get_data(res)
    assert tutor_algo_prog.first_name in data["firstName"]
    assert tutor_algo_prog.username in data["username"]
    

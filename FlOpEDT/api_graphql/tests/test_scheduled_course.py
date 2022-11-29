from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from people.models import Tutor
from base.models import Week, Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_modules import module_algo_prog, module_conception_log, training_l3_miashs ,training_l2_miashs, \
department_miashs, period_1 , period_2, tutor_algo_prog, tutor_conception
from test_user_preference import week1, week7
from lib import *

@pytest.fixture
def course_type_algo(db) -> CourseType:
    return CourseType.objects.create(name= "Algo")

@pytest.fixture
def room_algo(db) -> Room:
    return Room.objects.create( name="B101")

@pytest.fixture
def course_algo(db, module_algo_prog: Module, course_type_algo: CourseType, week7 : Week) -> Course:
    return Course.objects.create(module=module_algo_prog, type= course_type_algo, week = week7)


@pytest.fixture
def scheduled1(db, tutor_algo_prog:Tutor,
                room_algo:Room,
                course_algo:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_algo_prog, room= room_algo, course= course_algo, start_time = 5)

@pytest.fixture
def course_type_conception(db) -> CourseType:
    return CourseType.objects.create(name= "Conception") 

@pytest.fixture
def room_algo(db) -> Room:
    return Room.objects.create( name="B101")

@pytest.fixture
def room_conception(db) -> Room:
    return Room.objects.create( name="Z909")

@pytest.fixture
def course_conception(db, module_conception_log: Module, course_type_conception:CourseType, week1 : Week) -> Course:
    return Course.objects.create(module=module_conception_log, type= course_type_conception, week = week1)

@pytest.fixture
def scheduled2(db, tutor_conception:Tutor,
                room_conception:Room,
                course_conception:Course) -> ScheduledCourse:
    return ScheduledCourse.objects.create(tutor= tutor_conception, room= room_conception, course= course_conception, start_time = 2)


def test_scheduled_course(client_query,
                        scheduled1 : ScheduledCourse, scheduled2 : ScheduledCourse):
    query = '''
        query {
            scheduledCourses (week: 7, year : 2021) {
                edges {
                    node {
                        tutor{
                            username
                        }   
                        room{
                            name
                        }
                        course{
                            type {
                                name
                            }
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "scheduledCourses")
    data = get_data(res)
    assert scheduled1.tutor.username in data["username"]
    assert scheduled1.room.name in data["name"]
    assert scheduled1.course.type.name in data["name"]
    assert scheduled2.tutor.username not in data["username"]
    assert scheduled2.room.name not in data["name"]
    assert scheduled2.course.type.name not in data["name"]


    

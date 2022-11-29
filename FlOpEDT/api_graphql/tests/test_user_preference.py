from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import UserPreference, Week
from people.models import Tutor
from base.timing import Day
from base.models import Week, Course,Room, ScheduledCourse, CourseType, Module, TrainingProgramme, Department, Period
from test_modules import department_miashs, tutor_algo_prog, tutor_conception
from lib import *

@pytest.fixture
def week1(db) -> Week:
    return Week.objects.create(nb=1, year=2022)

@pytest.fixture
def week7(db) -> Week:
    return Week.objects.create(nb=7, year=2021)

@pytest.fixture
def user_pref_algo_prog(db, \
    tutor_algo_prog : Tutor, week7 : Week) -> UserPreference:
    return UserPreference.objects.create(
        user = tutor_algo_prog,week = week7,
        start_time = 2, duration = 3,
        day = Day.THURSDAY, value = 5 
    )

@pytest.fixture
def user_pref_conception(db, \
    tutor_conception : Tutor, week1 : Week) -> UserPreference:
    return UserPreference.objects.create(
        user = tutor_conception,week = week1,
        start_time = 1, duration = 1,
        day = Day.FRIDAY, value = 2 
    )

def test_all_user_pref(client_query,
                    user_pref_algo_prog : UserPreference, 
                    user_pref_conception : UserPreference):
    query = '''
        query {
            userPreferences {
                edges {
                    node {
                        day
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "userPreferences")
    data = get_data(res)
    assert user_pref_algo_prog.day.upper() in data["day"]
    assert user_pref_conception.day.upper() in data["day"]

def test_user_pref_with_filters_1(client_query,
                                user_pref_conception : UserPreference):
    query = '''
        query {
            userPreferences (dept : \"MIASHS\", week_Year : 2022) {
                edges {
                    node {
                        value
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "userPreferences")
    data = get_data(res)
    assert user_pref_conception.value in data["value"]
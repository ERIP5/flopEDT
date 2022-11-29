from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Module, TrainingProgramme, Department, Period
from people.models import Tutor
from lib import *

@pytest.fixture
def department_miashs(db) -> Department:
    return Department.objects.create(abbrev="MIASHS", name="Maths Info - SHS")

@pytest.fixture
def training_l2_miashs(db, department_miashs: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L2M", name="L2 MIASHS",
        department=department_miashs)

@pytest.fixture
def training_l3_miashs(db, department_miashs: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="L3M", name="L3 MIASHS",
        department=department_miashs)

@pytest.fixture
def period_1(db, department_miashs: Department)-> Period:
    return Period.objects.create(
        name="P1", department=department_miashs,
        starting_week=4, ending_week=7)

@pytest.fixture
def period_2(db, department_miashs: Department)-> Period:
    return Period.objects.create(
        name="P2", department=department_miashs,
        starting_week=1, ending_week=4)

@pytest.fixture
def tutor_conception(db, department_miashs : Department) -> Tutor:
    res = Tutor.objects.create(username="JD", first_name="John")
    res.save()
    res.departments.add(department_miashs)
    res.save()
    return res

@pytest.fixture
def tutor_algo_prog(db, department_miashs : Department) -> Tutor:
    res = Tutor.objects.create(username="EM", first_name="Elon")
    res.save()
    res.departments.add(department_miashs)
    res.save()
    return res

@pytest.fixture
def module_conception_log(db, 
training_l3_miashs : TrainingProgramme, tutor_conception : Tutor, period_1 : Period) -> Module:
    return Module.objects.create(abbrev="CPTLog", name="Conception logiciel",
    head=tutor_conception, ppn="azertyuiop", 
    train_prog=training_l3_miashs, period=period_1,
    url="https://cptlog.com",
    description="Lorem ipsum dolor sit amet. In atque alias et eveniet provident eos nisi quisquam quo voluptatem tempore sed voluptas veritatis. Est sint tempore et voluptas accusantium qui ipsam fugiat. In similique eius eos debitis inventore sed nesciunt sint!")

@pytest.fixture
def module_algo_prog(db,
training_l2_miashs : TrainingProgramme, tutor_algo_prog : Tutor, period_2 : Period) -> Module:
    return Module.objects.create(abbrev="ALPG", name="Algo et prog",
    head=tutor_algo_prog, ppn="qsdfghjk", 
    train_prog=training_l2_miashs, period=period_2,
    url="https://algoprog.com",
    description="Est itaque obcaecati id aperiam optio cum praesentium vitae id doloribus aliquid? Et amet culpa ut esse harum aut quisquam aliquam et nemo aperiam et illo internos est Quis eaque non expedita dolor. Ut libero dolor est quasi ipsa At voluptatem alias qui distinctio voluptate sit cupiditate itaque ab vero possimus non quidem quis.")


def test_all_modules(client_query,
                    module_conception_log : Module, 
                    module_algo_prog : Module):
    query = '''
        query {
            modules (dept :\"MIASHS\"){
                edges {
                    node {
                        abbrev
                        head {
                            username
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "modules")
    data = get_data(res)
    assert module_conception_log.abbrev in data["abbrev"]
    assert module_algo_prog.abbrev in data["abbrev"]
    assert module_conception_log.head.username in data["username"]
    assert module_algo_prog.head.username in data["username"]

def test_modules_with_filters_1(client_query,
                                module_conception_log: Module):
    query = '''
        query {
            modules (dept :\"MIASHS\", week : 5) {
                edges {
                    node {
                        url
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "modules")
    data = get_data(res)
    assert module_conception_log.url in data["url"]

def test_modules_with_filters_2(client_query,
                                module_algo_prog: Module):
    query = '''
        query {
            modules (dept :\"MIASHS\", name_Icontains : \"l\",
            trainProg_Abbrev : \"L2M\") {
                edges {
                    node {
                        url
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "modules")
    data = get_data(res)
    assert module_algo_prog.url in data["url"]

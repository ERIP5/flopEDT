import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
import lib

from base.models import UserPreference, Week
from people.models import Tutor
from .test_tutor import tutor_info, tutor_reseaux
from .test_modules import tutor_algo_prog, tutor_conception


@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs,
                             client=client,
                             graphql_url="/graphql")

    return func

@pytest.fixture
def week_

"""
# Une fixture pour un department
@pytest.fixture
def department_miashs(db) -> Department:
    return Department.objects.create(abbrev="MIASHS", name="Maths Info - SHS")

# Des fixtures pour des trainingProgramme
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

# Des fixtures pour des periods
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

# Des fixtures pour des tutors
@pytest.fixture
def tutor_conception(db) -> Tutor:
    return Tutor.objects.create(username="JD", first_name="John")

@pytest.fixture
def tutor_algo_prog(db) -> Tutor:
    return Tutor.objects.create(username="EM", first_name="Elon")

# Des fixtures pour des modules
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
    head=tutor_algo_prog, ppn="azertyuiop", 
    train_prog=training_l2_miashs, period=period_2,
    url="https://algoprog.com",
    description="Est itaque obcaecati id aperiam optio cum praesentium vitae id doloribus aliquid? Et amet culpa ut esse harum aut quisquam aliquam et nemo aperiam et illo internos est Quis eaque non expedita dolor. Ut libero dolor est quasi ipsa At voluptatem alias qui distinctio voluptate sit cupiditate itaque ab vero possimus non quidem quis.")

def test_all_modules(client_query,
                    module_conception_log : Module, 
                    module_algo_prog : Module):
    lib.test_all (client_query, "modules", None, None, "abbrev", 
    m1 = module_conception_log,
    m2 = module_algo_prog)

def test_modules_filtered(client_query,
                                module_algo_prog: Module):
    lib.test_all (client_query, "modules", "name_Istartswith", '"Al"', "description", m1 = module_algo_prog)
    """
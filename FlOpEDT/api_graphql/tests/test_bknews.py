from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from displayweb.models import BreakingNews
from base.models import Department, Week, ModuleTutorRepartition
from test_tutor import department_info, department_reseaux
from lib import *




#parametre test
@pytest.fixture
def y1(db, department_info:Department) -> BreakingNews:
    return BreakingNews.objects.create(department= department_info , week = Week(year=2021, nb=11), y=5, txt = "Lorem ipsum dolor sit amet.")

@pytest.fixture
def y2(db, department_reseaux:Department) -> BreakingNews:
    return BreakingNews.objects.create(department= department_reseaux, week = Week(year=2022, nb=15), y=10, txt = "In atque alias et eveniet provident eos")

def test_bknews(client_query,
                    y1 : BreakingNews,
                    y2 : BreakingNews):
    query='''
        query{
            bknews {
                edges {
                    node {
                        y
                        txt
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "bknews")
    data = get_data(res)
    assert y1.y in data["y"]
    assert y2.y in data["y"]
    assert y1.txt in data["txt"]
    assert y2.txt in data["txt"]

def test_bknews_filters1(client_query,
                    y1 : BreakingNews):
    query='''
        query{
            bknews (department_Name_Istartswith : \"inf\", week : 11, year : 2021, y : 5) {
                edges {
                    node {
                        txt
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "bknews")
    data = get_data(res)
    assert y1.txt in data["txt"]
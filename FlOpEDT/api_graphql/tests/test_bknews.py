from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from displayweb.models import BreakingNews
from base.models import Department, Week, ModuleTutorRepartition
from test_tutor import department_info, department_reseaux
from lib import *
from test_user_preference import week1, week7




#parametre test
@pytest.fixture
def y1(db, department_info:Department, week1 : Week) -> BreakingNews:
    return BreakingNews.objects.create(department= department_info , week = week1, y=5, txt = "Lorem ipsum dolor sit amet.")

@pytest.fixture
def y2(db, department_reseaux:Department, week7 : Week) -> BreakingNews:
    return BreakingNews.objects.create(department= department_reseaux, week = week7, y=10, txt = "In atque alias et eveniet provident eos")

def test_bknews(client_query,
                    y1 : BreakingNews,
                    y2 : BreakingNews):
    query='''
        query{
            bknews {
                edges {
                    node {
                        week
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
    assert "week" in data
    assert y1.week.nb == data["week"]["nb"]
    assert y2.week in data["week"]

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
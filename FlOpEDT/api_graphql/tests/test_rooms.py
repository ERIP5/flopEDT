from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Room, Department, RoomType
from test_tutor import department_info, department_reseaux
from lib import *

@pytest.fixture
def room_type_info(db, \
    department_info : Department) -> RoomType:
    return RoomType.objects.create(
        department = department_info,
        name = "Salle de conference"
    )

@pytest.fixture
def room_type_reseaux(db, \
    department_reseaux : Department) -> RoomType:
    return RoomType.objects.create(
        department = department_reseaux,
        name = "Salle de cours"
    )

@pytest.fixture
def room_reseaux(db, \
    department_reseaux : Department, \
    room_type_reseaux : RoomType) -> Room:
    res = Room.objects.create(
       name = "RT069"
    )
    res.save()
    res.departments.add(department_reseaux)
    res.types.add(room_type_reseaux)
    return res

@pytest.fixture
def room_info(db, \
    department_info : Department, \
    room_type_info : RoomType) -> Room:
    res = Room.objects.create(
       name = "INF407"
    )
    res.save()
    res.departments.add(department_info)
    res.types.add(room_type_info)
    return res

def test_room(client_query, 
                    room_info : Room):
    query = '''
        query {
            rooms (dept : \"INFO\", name_Icontains : \"INF\") {
                edges{
                    node{
                	    name
                        departments {
                            edges {
                                node {
                                    name
                                    abbrev
                                }
                            }
                        }
                    }
                }
            }
        }
    '''
    res = execute_query (client_query, query, "rooms")
    data = get_data(res) 
    assert room_info.name in data["name"] 
    for d in list(room_info.departments.all()):
        assert d.name in data["name"]
        assert d.abbrev in data["abbrev"]
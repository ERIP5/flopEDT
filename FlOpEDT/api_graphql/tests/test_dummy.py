# Create a fixture using the graphql_query helper
# and `client` fixture from `pytest-django`.
import json
from _pytest.fixtures import fixture
import pytest
from graphene_django.utils.testing import graphql_query
from base.models import Department, TrainingProgramme
from lib import *



# Pour pouvoir faire des requêtes sur graphQL pendant les tests
# Insatisfaisant car graphql_url devrait venir de la configuration globale
# mais on s'en contentera

# Des fixtures pour des départements
@pytest.fixture
def department_info(db) -> Department:
    return Department.objects.create(abbrev="CS", name="Computer Science")

@pytest.fixture
def department_socio(db) -> Department:
    return Department.objects.create(abbrev="So", name="Sociology")

# Des training programme avec une factory
@pytest.fixture
def trainprog_info_factory(db, department_info: Department):
    def create_training_programme_info(
            abbrev: str,
            name:str)  -> TrainingProgramme:
        return TrainingProgramme.objects.create(
            abbrev=abbrev, name=name,
            department=department_info)
    return create_training_programme_info

@pytest.fixture
def trainprog_info_A(db, trainprog_info_factory):
    return trainprog_info_factory(abbrev="CSA", name="Computer Science A")

@pytest.fixture
def trainprog_info_B(db, trainprog_info_factory):
    return trainprog_info_factory(abbrev="CSB", name="Computer Science B")

# Des training programme sans factory
@pytest.fixture
def trainprog_socio_A(db, department_socio: Department) -> TrainingProgramme:
    return TrainingProgramme.objects.create(
        abbrev="SoA", name="Sociology A",
        department=department_socio)


# Test d'un première requête
# (Avec une List dans le type TrainingProgrammeQL)
def test_all_training_programmes(client_query,
                                 trainprog_info_A: TrainingProgramme,
                                 trainprog_info_B: TrainingProgramme,
                                 trainprog_socio_A: TrainingProgramme):
    response = client_query(
        '''
        query {
          trainingProgrammes(weekNb:10, weekYy:2025) {
            abbrev
          }
        }
        '''
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    # pas très nécessaire
    # assert "trainingProgrammes" in content["data"]
    training_programmes = content["data"]["trainingProgrammes"]
    assert len(training_programmes) == 3
    assert (set([tp["abbrev"] for tp in training_programmes])
            == set([tp.abbrev for tp in [trainprog_info_A, trainprog_info_B,
                                         trainprog_socio_A]]))

# Test d'un première requête
# (Avec une List dans le type TrainingProgrammeQL)
def test_all_departments(client_query,
                         department_info: Department,
                         department_socio: Department):
    response = client_query(
        '''
        query {
          departments(name_Istartswith: "Soc") {
            edges {
              node {
                abbrev
                name
              }
            }
          }
        }
        '''
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    # pas très nécessaire
    # assert "departments" in content["data"]
    # assert "edges" in content["data"]["departments"]
    nodes = content["data"]["departments"]["edges"]
    assert len(nodes) == 1
    # pas très nécessaire
    # assert "node" in nodes[0]
    node = nodes[0]["node"]
    assert node["abbrev"] == department_socio.abbrev


# Test de récupération d'un dictionnaire
def test_(client_query):
    response = client_query(
        '''
        query {
          dictionary {
            out
          }
        }
        '''
    )
    content = json.loads(response.content)
    assert "errors" not in content
    assert "dictionary" in content["data"]
    assert "out" in content["data"]["dictionary"]
    out = content["data"]["dictionary"]["out"]
    assert out == {
        "pouet":{
            "w": 10
        },
        "poot": 11
    }


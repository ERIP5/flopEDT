from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import TrainingProgrammeType

class Query(BaseQuery):
    trainingprogrammes = DjangoFilterConnectionField(TrainingProgrammeType)

from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import TutorType

class Query(BaseQuery):
    tutors = DjangoFilterConnectionField(TutorType)


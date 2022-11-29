from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import WeekType

class Query(BaseQuery):
    weeks = DjangoFilterConnectionField(WeekType)
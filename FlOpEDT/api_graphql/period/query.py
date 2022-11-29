from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import PeriodType

class Query(BaseQuery):
    periods = DjangoFilterConnectionField(PeriodType)
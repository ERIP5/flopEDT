from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import GroupTypeNode

class Query(BaseQuery):
    groupTypes = DjangoFilterConnectionField(GroupTypeNode)

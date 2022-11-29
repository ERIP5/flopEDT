from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import GenericGroupNode

class Query(BaseQuery):
    genericGroups = DjangoFilterConnectionField(GenericGroupNode)

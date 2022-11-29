from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import ModuleNode

class Query(BaseQuery):
    modules = DjangoFilterConnectionField(ModuleNode)
    

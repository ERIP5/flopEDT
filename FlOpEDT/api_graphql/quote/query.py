from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import QuoteNode

class Query(BaseQuery):
    quotes = DjangoFilterConnectionField(QuoteNode)
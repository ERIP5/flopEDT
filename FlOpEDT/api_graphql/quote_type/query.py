from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery

from .types import QuoteTypeNode

class Query(BaseQuery):
    quoteTypes = DjangoFilterConnectionField(QuoteTypeNode)

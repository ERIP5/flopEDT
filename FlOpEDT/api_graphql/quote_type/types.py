from graphene import relay
from graphene_django import DjangoObjectType
from quote.models import QuoteType
from .filter import QuoteTypeFilter

class QuoteTypeNode(DjangoObjectType):

    class Meta:
        model = QuoteType
        filterset_class = QuoteTypeFilter
        interfaces = (relay.Node, )
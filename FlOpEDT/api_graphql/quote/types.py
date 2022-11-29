from graphene import relay
from graphene_django import DjangoObjectType
from quote.models import Quote
from .filter import QuoteFilter

class QuoteNode(DjangoObjectType):
    class Meta:
        model = Quote
        filterset_class = QuoteFilter
        interfaces = (relay.Node, )

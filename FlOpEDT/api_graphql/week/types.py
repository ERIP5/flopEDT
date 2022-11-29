from graphene import relay
from graphene_django import DjangoObjectType
from base.models import Week
from .filter import WeekFilter

class WeekType(DjangoObjectType):
    class Meta:
        model = Week
        filterset_class = WeekFilter
        interfaces = (relay.Node, )
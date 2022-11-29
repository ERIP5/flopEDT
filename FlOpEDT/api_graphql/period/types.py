from graphene import relay
from graphene_django import DjangoObjectType
from base.models import Period
from .filter import PeriodFilter

class PeriodType(DjangoObjectType):
    class Meta:
        model = Period
        filterset_class = PeriodFilter
        interfaces = (relay.Node, )
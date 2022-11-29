from graphene import relay
from graphene_django import DjangoObjectType
from base.models import GenericGroup
from .filter import GenericGroupFilter

class GenericGroupNode(DjangoObjectType):
    class Meta:
        model = GenericGroup
        filterset_class = GenericGroupFilter
        interfaces = (relay.Node, )

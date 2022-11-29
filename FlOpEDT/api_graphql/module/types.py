from graphene import relay
from graphene_django import DjangoObjectType
from base.models import Module
from .filter import ModuleFilter

class ModuleNode(DjangoObjectType):
    class Meta:
        model = Module
        filterset_class = ModuleFilter
        interfaces = (relay.Node, )

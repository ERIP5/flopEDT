from graphene import relay
from graphene_django import DjangoObjectType
from base.models import GroupType
from.filter import GroupTypeFilter

class GroupTypeNode(DjangoObjectType):
    class Meta:
        model = GroupType
        filterset_class = GroupTypeFilter
        interfaces = (relay.Node, )

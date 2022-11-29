from graphene import relay
from graphene_django import DjangoObjectType
from base.models import RoomType
from .filter import RoomTypeFilter

class RoomTypeNode(DjangoObjectType):
    class Meta:
        model = RoomType
        filterset_class = RoomTypeFilter
        interfaces = (relay.Node, )
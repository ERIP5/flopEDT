from graphene import relay
from graphene_django import DjangoObjectType
from base.models import Room
from .filter import RoomFilter

class RoomNode(DjangoObjectType):
    class Meta:
        model = Room
        filterset_class = RoomFilter
        interfaces = (relay.Node, )

from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import RoomNode

class Query(BaseQuery):
    rooms = DjangoFilterConnectionField(RoomNode)

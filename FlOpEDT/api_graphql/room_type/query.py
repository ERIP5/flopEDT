from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import RoomTypeNode

class Query(BaseQuery):
    roomTypes = DjangoFilterConnectionField(RoomTypeNode)

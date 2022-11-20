from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import BknewsType

class Query (BaseQuery):
    bknews = DjangoFilterConnectionField(
        BknewsType,
        description = "A list of breaking news",
        resolver = resolve.all_bknews
    )

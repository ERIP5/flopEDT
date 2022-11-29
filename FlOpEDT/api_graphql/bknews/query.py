from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery

from .types import BknewsType

class Query (BaseQuery):
    bknews = DjangoFilterConnectionField(
        BknewsType,
        description = "A list of breaking news",
    )

from graphene import List
from graphene_django.filter import DjangoFilterConnectionField

from api_graphql.base import BaseQuery
from . import resolvers as resolve

from .types import DepartmentType

class Query(BaseQuery):
    departments = DjangoFilterConnectionField(
        DepartmentType,
        description = "A list of departments",
        resolver = resolve.all_departments
    )


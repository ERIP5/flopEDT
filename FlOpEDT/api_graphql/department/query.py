from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import DepartmentType

class Query(BaseQuery):
    departments = DjangoFilterConnectionField(
        DepartmentType,
        description = "A list of departments",
    )

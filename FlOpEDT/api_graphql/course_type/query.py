from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery

from .types import CourseTypeNode

class Query(BaseQuery):
    courseTypes = DjangoFilterConnectionField(CourseTypeNode)

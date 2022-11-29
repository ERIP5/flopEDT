from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import CourseNode

class Query(BaseQuery):
    courses = DjangoFilterConnectionField(CourseNode)

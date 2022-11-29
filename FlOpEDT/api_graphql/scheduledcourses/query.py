from graphene_django.filter import DjangoFilterConnectionField
from api_graphql.base import BaseQuery
from .types import ScheduledCourseNode

class Query(BaseQuery):
    scheduledCourses = DjangoFilterConnectionField(ScheduledCourseNode)
    

from graphene import relay
from graphene_django import DjangoObjectType
from .filter import CourseFilter
from base.models import Course

class CourseNode(DjangoObjectType):
    class Meta:
        model = Course
        filterset_class = CourseFilter
        interfaces = (relay.Node, )

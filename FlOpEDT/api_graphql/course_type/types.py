from graphene import relay
from graphene_django import DjangoObjectType
from base.models import CourseType
from .filter import CourseTypeFilter

class CourseTypeNode(DjangoObjectType):
    class Meta:
        model = CourseType
        filterset_class = CourseTypeFilter
        interfaces = (relay.Node, )

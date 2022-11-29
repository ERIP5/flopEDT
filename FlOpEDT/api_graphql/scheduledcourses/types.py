from graphene import relay
from graphene_django import DjangoObjectType
from base.models import ScheduledCourse
from .filter import ScheduledCourseFilter

class ScheduledCourseNode(DjangoObjectType):
    class Meta:
        model = ScheduledCourse    
        filterset_class = ScheduledCourseFilter
        interfaces = (relay.Node, )
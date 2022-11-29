from graphene import relay
from graphene_django import DjangoObjectType
from people.models import Tutor
from .filter import TutorFilter

class TutorType(DjangoObjectType):

    class Meta:
        model = Tutor
        filterset_class = TutorFilter
        interfaces = (relay.Node, )
from graphene import relay
from graphene_django import DjangoObjectType
from base.models import TrainingProgramme
from .filter import TrainingProgrammeFilter

class TrainingProgrammeType(DjangoObjectType):
    class Meta:
        model = TrainingProgramme
        filterset_class = TrainingProgrammeFilter
        interfaces = (relay.Node, )

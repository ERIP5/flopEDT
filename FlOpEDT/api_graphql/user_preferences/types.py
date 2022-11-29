from graphene import relay
from graphene_django import DjangoObjectType
from base.models import UserPreference
from .filter import UserPreferenceFilter

class UserPreferenceNode(DjangoObjectType):
    class Meta:
        model = UserPreference
        filterset_class = UserPreferenceFilter
        interfaces = (relay.Node, )
from graphene import relay
from graphene_django import DjangoObjectType
from base.models import Department
from .filter import DepartmentFilter

class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department
        filterset_class = DepartmentFilter
        interfaces = (relay.Node, )
        

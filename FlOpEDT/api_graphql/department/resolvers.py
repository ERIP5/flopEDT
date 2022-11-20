from base.models import Department
#from base.models import Department, Week

def all_departments(root, info):
    return Department.objects.all()

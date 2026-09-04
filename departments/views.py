from rest_framework.viewsets import ModelViewSet
from departments.models import Department
from departments.serializers import DepartmentSerializer
from departments.permissions import IsAdminOrReadOnly

class DepartmentViewSets(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'uuid'

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]


    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.action == 'list':
            return Usuario.objects.filter(id=self.request.user.id)
        return Usuario.objects.all()

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        if password:
            serializer.save(password=password)
        else:
            serializer.save()
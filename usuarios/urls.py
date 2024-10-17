from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, LicaoViewSet, editar_html

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'licoes', LicaoViewSet, basename='licao')

urlpatterns = [
    path('', include(router.urls)),
    path('licoes/<int:id>/editar-html/', editar_html, name='editar-html'),
]

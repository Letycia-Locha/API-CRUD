from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, editar_html

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

usuario_list = UsuarioViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

usuario_detail = UsuarioViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path('usuarios/', usuario_list, name='usuario-list'),
    path('usuarios/<int:pk>/', usuario_detail, name='usuario-detail'),
    path('licoes/<int:id>/editar-html/', editar_html, name='editar-html'),
]
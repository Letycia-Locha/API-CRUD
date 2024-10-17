from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from .models import Usuario, Licao
from .serializers import UsuarioSerializer, LicaoSerializer
from bs4 import BeautifulSoup

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para garantir que apenas o proprietário do objeto possa editá-lo ou deletá-lo.
    """

    def has_object_permission(self, request, view, obj):
        # Permissão de leitura para qualquer requisição
        if request.method in permissions.SAFE_METHODS:
            return True

        # Se o objeto for do tipo Usuario, verificar se é o próprio usuário autenticado
        if isinstance(obj, Usuario):
            return obj == request.user

        # Se o objeto for do tipo Licao, verificar se o campo usuario é o usuário autenticado
        return obj.usuario == request.user

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'list':
            return Usuario.objects.filter(id=self.request.user.id)
        return Usuario.objects.all()

    def perform_create(self, serializer):
        try:
            # Cria a instância do usuário sem salvá-la ainda
            new_user = serializer.save()
            password = self.request.data.get('password')
            
            if password:
                new_user.set_password(password)  # Criptografa a senha
            else:
                raise ValidationError({"password": "O campo de senha é obrigatório."})

            new_user.save()  # Agora salva o usuário com a senha criptografada

            # Gera o token JWT para o usuário recém-criado
            refresh = RefreshToken.for_user(new_user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            # Adiciona os tokens aos dados da resposta
            self.response_data = {
                'user': UsuarioSerializer(new_user).data,
                'tokens': tokens,
            }

        except Exception as e:
            # Lança uma exceção de validação com a mensagem do erro
            raise ValidationError({"detail": f"Erro ao criar usuário: {str(e)}"})

    def create(self, request, *args, **kwargs):
        # Customiza a resposta da criação do usuário para incluir os tokens
        response = super().create(request, *args, **kwargs)
        if hasattr(self, 'response_data'):
            response.data = self.response_data
        return response

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def editar_html(request, id):
    try:
        licao = Licao.objects.get(pk=id)
    except Licao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Verificar se o usuário é o proprietário da lição
    if licao.usuario != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    # Modificar o conteúdo HTML
    html = licao.conteudo_html
    soup = BeautifulSoup(html, 'html.parser')

    # Exemplo de modificação: alterar a cor de um botão
    for button in soup.find_all('button'):
        button['style'] = 'background-color: blue; color: white;'

    # Adicionar função JavaScript
    script = soup.new_tag('script')
    script.string = '''
        function alertaClique() {
            alert('Botão clicado!');
        }
        document.querySelectorAll('button').forEach(button => {
            button.addEventListener('click', alertaClique);
        });
    '''
    soup.body.append(script)

    licao.conteudo_html = str(soup)
    licao.save()

    serializer = LicaoSerializer(licao)
    return Response(serializer.data)

class LicaoViewSet(viewsets.ModelViewSet):
    queryset = Licao.objects.all()
    serializer_class = LicaoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

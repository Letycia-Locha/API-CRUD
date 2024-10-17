from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Usuario, Licao
from .serializers import UsuarioSerializer, LicaoSerializer
from bs4 import BeautifulSoup

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editar_html(request, id):
    try:
        licao = Licao.objects.get(pk=id)
    except Licao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
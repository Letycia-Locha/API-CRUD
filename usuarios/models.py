from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    nome = models.CharField(_('nome'), max_length=150, blank=False, default='Usuario')
    email = models.EmailField(_('email address'), unique=True)
    data_de_nascimento = models.DateField(_('date of birth'), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome']

    def __str__(self):
        return self.email

class Licao(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo_html = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)  # Defina um valor padrão temporário

    def __str__(self):
        return self.titulo

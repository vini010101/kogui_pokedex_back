from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from .models import Usuario, TipoPokemon, PokemonUsuario
from .serializers import UsuarioSerializer, TipoPokemonSerializer, PokemonUsuarioSerializer


# ---- VIEWSETS ----

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]


class TipoPokemonViewSet(viewsets.ModelViewSet):
    queryset = TipoPokemon.objects.all()
    serializer_class = TipoPokemonSerializer
    permission_classes = [IsAuthenticated]


class PokemonUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PokemonUsuario.objects.all()
    serializer_class = PokemonUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retorna apenas os pokémons do usuário autenticado."""
        user = self.request.user
        return PokemonUsuario.objects.filter(IDUsuario__Login=user.username)

    def perform_create(self, serializer):
        """Associa automaticamente o Pokémon ao usuário autenticado."""
        user = self.request.user
        usuario = Usuario.objects.filter(Login=user.username).first()
        serializer.save(IDUsuario=usuario)


# ---- LOGIN ----

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    login = request.data.get('Login')
    senha = request.data.get('Senha')

    usuario = Usuario.objects.filter(Login=login).first()
    if usuario and check_password(senha, usuario.Senha):
        refresh = RefreshToken.for_user(usuario)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': UsuarioSerializer(usuario).data
        })
    return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

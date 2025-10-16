from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import JSONParser
from pokedex_project.swagger import register_user_schema, login_schema
from .models import Usuario, TipoPokemon, PokemonUsuario
from .serializers import UsuarioSerializer, TipoPokemonSerializer, PokemonUsuarioSerializer, RegisterSerializer


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
@login_schema
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    usuario = Usuario.objects.filter(Login=username).first()
    if usuario and check_password(password, usuario.Senha):
        refresh = RefreshToken.for_user(usuario)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': UsuarioSerializer(usuario).data
        })
    return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


@register_user_schema
@api_view(['POST'])
@parser_classes([JSONParser])
def register_user_view(request):
    serializer = RegisterSerializer(data=request.data)
    
    # Valida os dados enviados
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    # Verifica campos obrigatórios
    if not email or not username or not password:
        return Response(
            {'detail': 'Email, username e senha são obrigatórios'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verifica se email já existe
    if Usuario.objects.filter(email=email).exists():
        return Response(
            {'detail': 'Email já existe'}, 
            status=status.HTTP_409_CONFLICT
        )

    # Cria o usuário
    user = Usuario.objects.create_user(email=email, password=password, username=username)

    return Response(
        {
            'detail': 'Usuário criado com sucesso',
            'user_id': user.id,
            'email': user.email,
            'username': user.username
        }, 
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_pokemons_view(request):
    """
    Lista os Pokémons do usuário autenticado.
    Filtros opcionais:
      - ?nome=pikachu
      - ?codigo=25
    """
    user = request.user
    nome = request.query_params.get('nome')
    codigo = request.query_params.get('codigo')

    queryset = PokemonUsuario.objects.filter(IDUsuario__Login=user.username)

    if nome:
        queryset = queryset.filter(Nome__icontains=nome)
    if codigo:
        queryset = queryset.filter(Codigo=codigo)

    serializer = PokemonUsuarioSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_favoritos_view(request):
    """
    Retorna todos os Pokémons marcados como favoritos do usuário autenticado.
    """
    user = request.user
    favoritos = PokemonUsuario.objects.filter(IDUsuario__Login=user.username, Favorito=True)
    serializer = PokemonUsuarioSerializer(favoritos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_equipe_view(request):
    """
    Retorna os Pokémons que estão na equipe de batalha (máximo 6).
    """
    user = request.user
    equipe = PokemonUsuario.objects.filter(IDUsuario__Login=user.username, GrupoBatalha=True)[:6]
    serializer = PokemonUsuarioSerializer(equipe, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from pokedex_project.swagger import (
    listar_pokemons_schema,
    listar_favoritos_schema,
    listar_equipe_schema,
    adicionar_pokemon_schema,
    login_schema,
    register_user_schema,
    atualizar_equipe_schema,
    atualizar_favorito_schema
)
from .models import Usuario, TipoPokemon, PokemonUsuario
from .serializers import (
    UsuarioSerializer,
    TipoPokemonSerializer,
    PokemonUsuarioSerializer,
    RegisterSerializer,
    LoginSerializer
)
from .services import get_pokemon


# ==== VIEWSETS ====

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


# ==== AUTENTICAÇÃO ====

@login_schema
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'detail': 'Login e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    usuario = authenticate(request, username=username, password=password)
    if not usuario:
        return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(usuario)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'usuario': UsuarioSerializer(usuario).data
    })


@register_user_schema
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def register_user_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    if not email or not username or not password:
        return Response(
            {'detail': 'Email, username e senha são obrigatórios'},
            status=status.HTTP_400_BAD_REQUEST 
        )

    if Usuario.objects.filter(Email=email).exists():
        return Response({'detail': 'Email já existe'}, status=status.HTTP_409_CONFLICT)

    # Criação segura do usuário
    user = Usuario(
        Email=email,
        Login=username
    )
    user.set_password(password)
    user.save()

    return Response(
        {
            'detail': 'Usuário criado com sucesso',
            'user_id': user.IDUsuario,
            'email': user.Email,
            'username': user.Login
        },
        status=status.HTTP_201_CREATED
    )

# ==== FUNCIONALIDADES POKÉDEX ====
@listar_pokemons_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_pokemons_view(request):
    """
    Lista Pokémons da PokéAPI.
    Filtros opcionais:
      - ?nome=pikachu
      - ?codigo=25
    """
    nome = request.query_params.get('nome')
    codigo = request.query_params.get('codigo')

    pokemons = []

    # Definindo um range de IDs para buscar (exemplo: 1 a 150)
    for poke_id in range(1, 25):
        data = get_pokemon(poke_id)
        if not data:
            continue

        poke_nome = data['name']

        # Filtros
        if nome and nome.lower() not in poke_nome.lower():
            continue
        if codigo and str(codigo) != str(data['id']):
            continue

        pokemons.append({
            'id': data['id'],
            'nome': poke_nome,
            'tipo': [t['type']['name'] for t in data['types']],
            'imagem': data['sprites']['front_default']
        })

    return Response(pokemons)

@adicionar_pokemon_schema
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adicionar_pokemon_view(request):
    """
    Adiciona um Pokémon à lista do usuário autenticado,
    buscando informações diretamente da PokéAPI.
    """
    nome_pokemon = request.data.get('nome_pokemon')
    if not nome_pokemon:
        return Response({'detail': 'Informe o nome do Pokémon'}, status=400)

    usuario = request.user  # Usuário autenticado via JWT

    dados = get_pokemon(nome_pokemon)
    if not dados:
        return Response({'detail': 'Pokémon não encontrado na PokéAPI'}, status=404)

    tipo_nome = dados['types'][0]['type']['name']
    tipo_obj, _ = TipoPokemon.objects.get_or_create(Descricao=tipo_nome)

    if PokemonUsuario.objects.filter(IDUsuario=usuario, Codigo=dados['id']).exists():
        return Response({'detail': 'Este Pokémon já está na sua lista'}, status=400)

    pokemon = PokemonUsuario.objects.create(
        IDUsuario=usuario,
        IDTipoPokemon=tipo_obj,
        Codigo=dados['id'],
        Nome=dados['name'],
        ImagemURL=dados['sprites']['front_default'],
        Favorito=False,
        GrupoBatalha=True
    )

    return Response({
        'id': pokemon.Codigo,
        'nome': pokemon.Nome,
        'tipo': tipo_nome,
        'imagem': pokemon.ImagemURL,
        'mensagem': f'{pokemon.Nome.capitalize()} adicionado com sucesso!'
    }, status=201)

@listar_favoritos_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_favoritos_view(request):
    """
    Retorna todos os Pokémons marcados como favoritos do usuário autenticado.
    """
    user = request.user
    favoritos = PokemonUsuario.objects.filter(IDUsuario__Login=user.Login, Favorito=True)
    serializer = PokemonUsuarioSerializer(favoritos, many=True)
    return Response(serializer.data)

@listar_equipe_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_equipe_view(request):
    """
    Retorna os Pokémons que estão na equipe de batalha (máximo 6).
    """
    usuario = request.user
    equipe = PokemonUsuario.objects.filter(IDUsuario=usuario, GrupoBatalha=True)[:6]
    serializer = PokemonUsuarioSerializer(equipe, many=True)
    return Response(serializer.data, status=200)



@atualizar_favorito_schema
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def atualizar_favorito_view(request, pokemon_id: int):
    """
    Marca ou desmarca um Pokémon como favorito.
    """
    user = request.user
    try:
        pokemon = PokemonUsuario.objects.get(IDUsuario__Login=user.Login, IDPokemonUsuario=pokemon_id)
    except PokemonUsuario.DoesNotExist:
        return Response({'detail': 'Pokémon não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Alterna o valor do favorito
    pokemon.Favorito = not pokemon.Favorito
    pokemon.save()

    return Response({
        'detail': f'{pokemon.Nome} {"marcado como favorito" if pokemon.Favorito else "removido dos favoritos"}',
        'pokemon': PokemonUsuarioSerializer(pokemon).data
    }, status=status.HTTP_200_OK)


@atualizar_equipe_schema
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def atualizar_equipe_view(request, pokemon_id: int):
    """
    Adiciona ou remove um Pokémon da equipe de batalha (máximo 6).
    """
    user = request.user
    try:
        pokemon = PokemonUsuario.objects.get(IDUsuario__Login=user.username, IDPokemonUsuario=pokemon_id)
    except PokemonUsuario.DoesNotExist:
        return Response({'detail': 'Pokémon não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if not pokemon.GrupoBatalha:
        # Verifica se o usuário já tem 6 pokémons na equipe
        count_equipe = PokemonUsuario.objects.filter(IDUsuario__Login=user.username, GrupoBatalha=True).count()
        if count_equipe >= 6:
            return Response({'detail': 'Você só pode ter 6 Pokémons na equipe'}, status=status.HTTP_400_BAD_REQUEST)

    pokemon.GrupoBatalha = not pokemon.GrupoBatalha
    pokemon.save()

    return Response({
        'detail': f'{pokemon.Nome} {"adicionado à equipe" if pokemon.GrupoBatalha else "removido da equipe"}',
        'pokemon': PokemonUsuarioSerializer(pokemon).data
    }, status=status.HTTP_200_OK)
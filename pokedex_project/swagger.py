# pokedex_project/swagger.py
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from pokedex_app.serializers import RegisterSerializer, PokemonUsuarioSerializer, LoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Informações da API
schema_info = openapi.Info(
    title="Kogui Pokedex API",
    default_version='v1',
    description="Documentação da API da Pokedex",
    contact=openapi.Contact(email="contato@seusite.com"),
    license=openapi.License(name="MIT License"),
)

# ===== Security Definitions globais para Swagger =====
SECURITY_DEFINITIONS = {
    'Bearer': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': 'Digite: Bearer <seu_token>'
    }
}



# Security scheme JWT (usado nos endpoints)
JWT_SECURITY = [{'Bearer': []}]

# Schema view
schema_view = get_schema_view(
    schema_info,
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[JWTAuthentication],  # <-- JWT aqui
)


# ==== Decorators swagger ====

register_user_schema = swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: 'Usuário criado', 400: 'Campos obrigatórios ausentes', 409: 'Email já existe'},
    security=[]  # Registro não precisa de JWT
)

login_schema = swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'Login realizado', 401: 'Credenciais inválidas'},
    security=[]  # Login não precisa de JWT
)

listar_pokemons_schema = swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('nome', openapi.IN_QUERY, description="Filtra pelo nome do Pokémon", type=openapi.TYPE_STRING),
        openapi.Parameter('codigo', openapi.IN_QUERY, description="Filtra pelo código do Pokémon", type=openapi.TYPE_INTEGER),
    ],
    responses={200: PokemonUsuarioSerializer(many=True)},
    security=JWT_SECURITY
)

adicionar_pokemon_schema = swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['nome_pokemon'],
        properties={
            'nome_pokemon': openapi.Schema(
                type=openapi.TYPE_STRING, 
                description="Nome do Pokémon a ser adicionado"
            )
        }
    ),
    responses={
        201: PokemonUsuarioSerializer(),
        400: 'Pokémon já na lista ou campo ausente',
        404: 'Pokémon não encontrado'
    },
    security=JWT_SECURITY
)

listar_favoritos_schema = swagger_auto_schema(
    method='get',
    responses={200: PokemonUsuarioSerializer(many=True)},
    security=JWT_SECURITY
)

listar_equipe_schema = swagger_auto_schema(
    method='get',
    responses={200: PokemonUsuarioSerializer(many=True)},
    security=JWT_SECURITY
)

atualizar_favorito_schema = swagger_auto_schema(
    method='patch',
    manual_parameters=[openapi.Parameter('pokemon_id', openapi.IN_PATH, description="ID do Pokémon", type=openapi.TYPE_INTEGER)],
    responses={200: PokemonUsuarioSerializer(), 404: 'Pokémon não encontrado'},
    security=JWT_SECURITY
)

atualizar_equipe_schema = swagger_auto_schema(
    method='patch',
    manual_parameters=[openapi.Parameter('pokemon_id', openapi.IN_PATH, description="ID do Pokémon", type=openapi.TYPE_INTEGER)],
    responses={200: PokemonUsuarioSerializer(), 400: 'Máximo de 6 Pokémons na equipe', 404: 'Pokémon não encontrado'},
    security=JWT_SECURITY
)

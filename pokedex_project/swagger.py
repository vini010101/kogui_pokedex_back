# pokedex_project/swagger.py
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from pokedex_app.serializers import RegisterSerializer, PokemonUsuarioSerializer, LoginSerializer

# Schema da API
schema_info = openapi.Info(
    title="Kogui Pokedex API",
    default_version='v1',
    description="Documentação da API da Pokedex",
    terms_of_service="https://www.seusite.com/terms/",
    contact=openapi.Contact(email="contato@seusite.com"),
    license=openapi.License(name="MIT License"),
)





# Schema view para Swagger / Redoc
schema_view = get_schema_view(
    schema_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Decoradores prontos para importar nas views
from drf_yasg.utils import swagger_auto_schema

register_user_schema = swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: 'Usuário criado', 400: 'Campos obrigatórios ausentes', 409: 'Email já existe'}
)

login_schema = swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: 'Login realizado', 401: 'Credenciais inválidas'}
)

listar_pokemons_schema = swagger_auto_schema(
    method='get',
    responses={200: PokemonUsuarioSerializer(many=True)}
)

listar_favoritos_schema = swagger_auto_schema(
    method='get',
    responses={200: PokemonUsuarioSerializer(many=True)}
)

listar_equipe_schema = swagger_auto_schema(
    method='get',
    responses={200: PokemonUsuarioSerializer(many=True)}
)

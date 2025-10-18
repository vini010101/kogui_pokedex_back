from django.urls import path
from .views import  login_view, listar_equipe_view, pokemon_detail_view, listar_pokemons_view, listar_favoritos_view, register_user_view, adicionar_pokemon_view, atualizar_equipe_view, atualizar_favorito_view

 # importa o schema_view para gerar a documentação da api, 
 # #centralizei todas ao urls dentro do arquivo de urls do app
from pokedex_project.swagger import schema_view 


urlpatterns = [

    path('api/login/', login_view, name='login'),
    path('api/register/', register_user_view, name='register_user'),
    path('api/pokemons/', listar_pokemons_view, name='listar_pokemons'),
    path('api/pokemons/favoritos/', listar_favoritos_view, name='listar_favoritos'),
    path('api/pokemons/equipe/', listar_equipe_view, name='listar_equipe'),
    path('api/pokemons/adicionar/', adicionar_pokemon_view, name='adicionar_pokemon'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/pokemons/<int:pokemon_id>/favorito/', atualizar_favorito_view, name='atulizar_favorito'),
    path('api/pokemons/<int:pokemon_id>/equipe/', atualizar_equipe_view, name='atualizar_equipe'),
    path('api/pokemons/<int:pokemon_id>/', pokemon_detail_view, name='pokemon-detail'),
]

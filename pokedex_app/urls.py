from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, TipoPokemonViewSet, PokemonUsuarioViewSet, login_view

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'tipos', TipoPokemonViewSet)
router.register(r'pokemons', PokemonUsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
]

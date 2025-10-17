from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from pokedex_app.services import get_pokemon
from pokedex_app.models import Usuario, TipoPokemon, PokemonUsuario

class PokemonServiceTest(TestCase):
    def test_get_pokemon_by_name(self):
        """Testa a função get_pokemon com nome"""
        resultado = get_pokemon("pikachu")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['name'], 'pikachu')
        self.assertIn('types', resultado)
    
    def test_get_pokemon_by_id(self):
        """Testa a função get_pokemon com ID"""
        resultado = get_pokemon(25)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['id'], 25)
        self.assertIn('types', resultado)

class PokemonAPITest(TestCase):
    def setUp(self):
        """Cria usuário e cliente para autenticação"""
        self.client = APIClient()
        self.usuario = Usuario.objects.create(
            Email='teste@teste.com',
            Login='teste_usuario'
        )
        self.usuario.set_password('123456')
        self.usuario.save()
        # Autenticação via JWT
        response = self.client.post('/login/', {'username': 'teste_usuario', 'password': '123456'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_pokemons_vazio(self):
        """Testa endpoint listar pokémons quando não há nenhum"""
        response = self.client.get('/api/pokemons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_adicionar_pokemon(self):
        """Testa adicionar um Pokémon via endpoint"""
        response = self.client.post('/api/pokemons/adicionar', {'nome_pokemon': 'pikachu'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['pokemon']['Nome'], 'pikachu')

    def test_listar_favoritos_vazio(self):
        response = self.client.get('/api/pokemons/favoritos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_listar_equipe_vazio(self):
        response = self.client.get('/api/pokemons/equipe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

from django.db import models


class TipoPokemon(models.Model):
    IDTipoPokemon = models.AutoField(primary_key=True)
    Descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.Descricao


class Usuario(models.Model):
    IDUsuario = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=100)
    Login = models.CharField(max_length=50, unique=True)
    Email = models.EmailField(unique=True)
    Senha = models.CharField(max_length=128)
    DtInclusao = models.DateTimeField(auto_now_add=True)
    DtAlteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Nome


class PokemonUsuario(models.Model):
    IDPokemonUsuario = models.AutoField(primary_key=True)
    IDUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pokemons")
    IDTipoPokemon = models.ForeignKey(TipoPokemon, on_delete=models.SET_NULL, null=True, related_name="pokemons")
    Codigo = models.CharField(max_length=50)  # código ou ID da PokéAPI
    Nome = models.CharField(max_length=100)
    ImagemURL = models.URLField(max_length=255, blank=True, null=True)
    GrupoBatalha = models.BooleanField(default=False)
    Favorito = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Nome} ({self.IDUsuario.Nome})"

    class Meta:
        verbose_name = "Pokémon do Usuário"
        verbose_name_plural = "Pokémons dos Usuários"

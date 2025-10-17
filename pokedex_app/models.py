from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin




class UsuarioManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Usuário precisa de um email")
        email = self.normalize_email(email)
        user = self.model(Login=login, Email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    IDUsuario = models.AutoField(primary_key=True)
    Nome = models.CharField(max_length=100)
    Login = models.CharField(max_length=50, unique=True)
    Email = models.EmailField(unique=True)
    DtInclusao = models.DateTimeField(auto_now_add=True)
    DtAlteracao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'Login'
    REQUIRED_FIELDS = ['Email']

    def __str__(self):
        return self.Nome










class TipoPokemon(models.Model):
    IDTipoPokemon = models.AutoField(primary_key=True)
    Descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.Descricao





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

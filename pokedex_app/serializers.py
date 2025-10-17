from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario, TipoPokemon, PokemonUsuario


class TipoPokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPokemon
        fields = ['IDTipoPokemon', 'Descricao']


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['IDUsuario', 'Nome', 'Login', 'Email', 'password', 'DtInclusao', 'DtAlteracao']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # set_password cuida do hash
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class PokemonUsuarioSerializer(serializers.ModelSerializer):
    IDUsuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    IDTipoPokemon = TipoPokemonSerializer(read_only=True)

    class Meta:
        model = PokemonUsuario
        fields = [
            'IDPokemonUsuario',
            'IDUsuario',
            'IDTipoPokemon',
            'Codigo',
            'Nome',
            'ImagemURL',
            'GrupoBatalha',
            'Favorito'
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True, min_length=6)

    def create(self, validated_data):
        # cria o usuário usando create_user do manager
        return Usuario.objects.create_user(
            login=validated_data['username'],  # mapeia username → Login
            email=validated_data['email'],
            password=validated_data['password']
        )
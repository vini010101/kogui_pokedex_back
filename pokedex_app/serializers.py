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
        fields = ['IDUsuario', 'Nome', 'Login', 'Email', 'Senha', 'DtInclusao', 'DtAlteracao']
        extra_kwargs = {'Senha': {'write_only': True}}

    def create(self, validated_data):
        validated_data['Senha'] = make_password(validated_data['Senha'])
        return super().create(validated_data)


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
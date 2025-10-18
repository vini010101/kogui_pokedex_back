Backend – Kogui Pokedex (Django + DRF + JWT)
# Kogui Pokedex - Backend

API REST para gerenciar Pokémons do usuário, autenticação JWT e integração com frontend.

## Tecnologias

- Python 3.13
- Django 5.x
- Django REST Framework
- DRF-YASG (Swagger)
- Simple JWT (Autenticação)
- SQLite (ou MySQL se quiser produção)
- Pipenv ou venv (gerenciamento de dependências)

## Pré-requisitos

- Python 3.13 instalado
- Pip ou Pipenv
- Git
- Node.js não necessário (somente frontend)
- Virtualenv recomendado

## Setup do ambiente

1. Clone o repositório:
```bash
git clone <URL_DO_REPO_BACKEND>
cd kogui_pokedex_back

2 Crie e ative o ambiente virtual:
python -m venv .venv
source .venv/bin/activate  # Linux / MacOS
.venv\Scripts\activate     # Windows

3 Instale as dependências:
pip install -r requirements.txt

4 Configure o banco de dados
Por padrão, usa SQLite (db.sqlite3).
Para MySQL, configure settings.py com suas credenciais.

5 Rode as migrations:
python manage.py migrate

6 Crie um superusuário (opcional, para admin):
python manage.py createsuperuser

7 Execute o servidor:
python manage.py runserver

O backend estará disponível em http://127.0.0.1:8000/.


Endpoints Principais
POST /api/register/ – Criar usuário
POST /api/login/ – Autenticar usuário e gerar JWT
GET /api/pokemons/ – Listar Pokémons (JWT necessário)
POST /api/pokemons/ – Adicionar Pokémon (JWT necessário)
GET /api/favoritos/ – Listar favoritos (JWT necessário)
GET /api/equipe/ – Listar equipe (JWT necessário)
PATCH /api/favoritos/<pokemon_id>/ – Atualizar favorito (JWT)
PATCH /api/equipe/<pokemon_id>/ – Atualizar equipe (JWT)

Projeto desenvolvido por mim. Agradeço desde já a oportunidade de demonstrar minhas habilidades em backend Python/Django.
ass: Vinicius Moura Engenheiro de Software

# 🔒 API de cadastro e autenticação de usuários

---

API REST de cadastro e autenticação de usuários escrito em Python (Django).

## 💻 Tecnologias e arquiteturas usadas

- Python
- Django
- SQLite
- REST
- JWT Authentication

## 📌 Endpoints

**POST** /api/register  
**POST** /api/login
**GET** /api/users  
**PATCH** /api/users/edit/<<int:user_id>>

---

## 🚀 Como executar

- **Localhost**:
  
  ```bash
  git clone https://github.com/levyaraujo/authenticator.git && cd authenticator
  ```
  
  ```bash
  python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
  ```
  
  ```bash
  python manage.py makemigrations && python manage.py migrate --run-syncdb && python manage.py runserver
  ```
  
  [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/21871412-ab337fb2-e011-4b39-ba22-edd8c6638675?action=collection%2Ffork&collection-url=entityId%3D21871412-ab337fb2-e011-4b39-ba22-edd8c6638675%26entityType%3Dcollection%26workspaceId%3Dd3d76c8a-813c-4dc5-b80d-a81079c2b913)
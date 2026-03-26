import pytest


def test_registrar_sucesso(client):
    res = client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "jogador1@teste.com", "senha": "senha123"},
    )
    assert res.status_code == 201
    dados = res.json()
    assert dados["nome_usuario"] == "jogador1"
    assert "id" in dados


def test_registrar_nome_duplicado(client):
    client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "j1@teste.com", "senha": "senha123"},
    )
    res = client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "outro@teste.com", "senha": "senha123"},
    )
    assert res.status_code == 400
    assert "Nome de usuário" in res.json()["mensagem"]


def test_registrar_email_duplicado(client):
    client.post(
        "/auth/registrar",
        json={"nome_usuario": "usuario_a", "email": "compartilhado@teste.com", "senha": "senha123"},
    )
    res = client.post(
        "/auth/registrar",
        json={"nome_usuario": "usuario_b", "email": "compartilhado@teste.com", "senha": "senha123"},
    )
    assert res.status_code == 400


def test_entrar_sucesso(client):
    client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "jogador1@teste.com", "senha": "senha123"},
    )
    res = client.post("/auth/entrar", json={"nome_usuario": "jogador1", "senha": "senha123"})
    assert res.status_code == 200
    dados = res.json()
    assert "token_acesso" in dados
    assert dados["tipo_token"] == "bearer"


def test_entrar_com_email(client):
    client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "jogador1@teste.com", "senha": "senha123"},
    )
    res = client.post(
        "/auth/entrar",
        json={"nome_usuario": "jogador1@teste.com", "senha": "senha123"},
    )
    assert res.status_code == 200


def test_entrar_senha_errada(client):
    client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "j1@teste.com", "senha": "senha123"},
    )
    res = client.post("/auth/entrar", json={"nome_usuario": "jogador1", "senha": "errada"})
    assert res.status_code == 401


def test_registrar_senha_curta(client):
    res = client.post(
        "/auth/registrar",
        json={"nome_usuario": "jogador1", "email": "j@teste.com", "senha": "123"},
    )
    assert res.status_code == 422

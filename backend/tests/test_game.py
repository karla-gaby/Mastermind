import pytest
from app.services.game_service import ServicoJogo


def test_avaliar_todos_exatos():
    exatos, cores = ServicoJogo._avaliar(["R", "G", "B", "Y"], ["R", "G", "B", "Y"])
    assert exatos == 4
    assert cores == 0


def test_avaliar_sem_acertos():
    exatos, cores = ServicoJogo._avaliar(["R", "R", "R", "R"], ["G", "G", "G", "G"])
    assert exatos == 0
    assert cores == 0


def test_avaliar_cores_certas_sem_exatos():
    exatos, cores = ServicoJogo._avaliar(["R", "G", "B", "Y"], ["G", "R", "Y", "B"])
    assert exatos == 0
    assert cores == 4


def test_avaliar_misto():
    exatos, cores = ServicoJogo._avaliar(["R", "G", "B", "Y"], ["R", "B", "G", "O"])
    assert exatos == 1  
    assert cores == 2    


def test_avaliar_cores_duplicadas():
    
    exatos, cores = ServicoJogo._avaliar(["R", "G", "B", "Y"], ["R", "R", "O", "O"])
    assert exatos == 1  
    assert cores == 0



def _registrar_e_entrar(client, nome="jogador", senha="senha123"):
    client.post(
        "/auth/registrar",
        json={"nome_usuario": nome, "email": f"{nome}@teste.com", "senha": senha},
    )
    res = client.post("/auth/entrar", json={"nome_usuario": nome, "senha": senha})
    return res.json()["token_acesso"]


def test_iniciar_jogo(client):
    token = _registrar_e_entrar(client)
    res = client.post("/jogos/iniciar", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 201
    dados = res.json()
    assert "jogo_id" in dados
    assert "codigo" in dados


def test_tentativa_cor_invalida(client):
    token = _registrar_e_entrar(client)
    jogo_id = client.post(
        "/jogos/iniciar", headers={"Authorization": f"Bearer {token}"}
    ).json()["jogo_id"]

    res = client.post(
        f"/jogos/{jogo_id}/tentativa",
        json={"tentativa": ["X", "G", "B", "Y"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


def test_tentativa_tamanho_errado(client):
    token = _registrar_e_entrar(client)
    jogo_id = client.post(
        "/jogos/iniciar", headers={"Authorization": f"Bearer {token}"}
    ).json()["jogo_id"]

    res = client.post(
        f"/jogos/{jogo_id}/tentativa",
        json={"tentativa": ["R", "G", "B"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 422


def test_tentativa_retorna_feedback(client):
    token = _registrar_e_entrar(client)
    jogo_id = client.post(
        "/jogos/iniciar", headers={"Authorization": f"Bearer {token}"}
    ).json()["jogo_id"]

    res = client.post(
        f"/jogos/{jogo_id}/tentativa",
        json={"tentativa": ["R", "G", "B", "Y"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    dados = res.json()
    assert "exatos" in dados
    assert "cores_certas" in dados
    assert dados["numero_tentativa"] == 1
    assert dados["status"] in ("ativo", "ganhou")


def test_buscar_estado_jogo(client):
    token = _registrar_e_entrar(client)
    jogo_id = client.post(
        "/jogos/iniciar", headers={"Authorization": f"Bearer {token}"}
    ).json()["jogo_id"]

    res = client.get(f"/jogos/{jogo_id}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    dados = res.json()
    assert dados["status"] == "ativo"
    assert "codigo_secreto" not in dados  


def test_endpoint_ranking(client):
    res = client.get("/ranking/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { ServicoAutenticacao } from './auth.service';

describe('ServicoAutenticacao', () => {
  let servico: ServicoAutenticacao;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ServicoAutenticacao,
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
      ],
    });
    servico = TestBed.inject(ServicoAutenticacao);
    httpMock = TestBed.inject(HttpTestingController);
    localStorage.clear();
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('deve ser criado', () => {
    expect(servico).toBeTruthy();
  });

  it('estaAutenticado() retorna false sem token', () => {
    expect(servico.estaAutenticado()).toBeFalse();
  });

  it('armazena token e usuário após autenticar()', () => {
    const mockResposta = {
      token_acesso: 'tok123',
      tipo_token: 'bearer',
      usuario_id: 1,
      nome_usuario: 'jogador1',
    };

    servico.autenticar({ nome_usuario: 'jogador1', senha: 'senha' }).subscribe();
    const req = httpMock.expectOne('http://localhost:8000/auth/entrar');
    expect(req.request.method).toBe('POST');
    req.flush(mockResposta);

    expect(servico.estaAutenticado()).toBeTrue();
    expect(servico.obterToken()).toBe('tok123');
    expect(servico.usuarioAtual()?.nome_usuario).toBe('jogador1');
  });

  it('limpa token e usuário ao sair()', () => {
    localStorage.setItem('mm_token', 'algum-token');
    servico.sair();
    expect(servico.estaAutenticado()).toBeFalse();
    expect(servico.obterToken()).toBeNull();
  });
});

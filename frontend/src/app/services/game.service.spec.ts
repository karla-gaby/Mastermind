import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { ServicoJogo } from './game.service';

describe('ServicoJogo', () => {
  let servico: ServicoJogo;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ServicoJogo,
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });
    servico = TestBed.inject(ServicoJogo);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('deve ser criado', () => {
    expect(servico).toBeTruthy();
  });

  it('iniciarJogo() faz POST em /jogos/iniciar', () => {
    const mockResposta = { jogo_id: 1, codigo: 'ABC12345', mensagem: 'Jogo iniciado!' };
    servico.iniciarJogo().subscribe((res) => {
      expect(res.jogo_id).toBe(1);
      expect(res.codigo).toBe('ABC12345');
    });
    const req = httpMock.expectOne('http://localhost:8000/jogos/iniciar');
    expect(req.request.method).toBe('POST');
    req.flush(mockResposta);
  });

  it('fazerTentativa() faz POST em /jogos/:id/tentativa', () => {
    const mockResposta = {
      exatos: 2, cores_certas: 1,
      numero_tentativa: 1, status: 'ativo', pontuacao: null,
    };
    servico.fazerTentativa(1, ['R', 'G', 'B', 'Y']).subscribe((res) => {
      expect(res.exatos).toBe(2);
      expect(res.cores_certas).toBe(1);
    });
    const req = httpMock.expectOne('http://localhost:8000/jogos/1/tentativa');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ tentativa: ['R', 'G', 'B', 'Y'] });
    req.flush(mockResposta);
  });

  it('buscarJogo() faz GET em /jogos/:id', () => {
    servico.buscarJogo(42).subscribe();
    const req = httpMock.expectOne('http://localhost:8000/jogos/42');
    expect(req.request.method).toBe('GET');
    req.flush({
      id: 42, codigo: 'XYZ', status: 'ativo',
      total_tentativas: 0, matriz_tentativas: [], pontuacao: 0,
      iniciado_em: new Date().toISOString(),
      finalizado_em: null, duracao_segundos: null,
    });
  });
});

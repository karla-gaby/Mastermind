export type Cor = 'R' | 'G' | 'B' | 'Y' | 'O' | 'P';
export type StatusJogo = 'ativo' | 'ganhou' | 'perdeu';

export const ROTULOS_COR: Record<Cor, string> = {
  R: 'Vermelho',
  G: 'Verde',
  B: 'Azul',
  Y: 'Amarelo',
  O: 'Laranja',
  P: 'Roxo',
};

export const CORES: Cor[] = ['R', 'G', 'B', 'Y', 'O', 'P'];

export interface RegistroTentativa {
  numero_tentativa: number;
  tentativa: Cor[];
  exatos: number;
  cores_certas: number;
}

export interface RespostaInicioJogo {
  jogo_id: number;
  codigo: string;
  mensagem: string;
}

export interface RespostaTentativa {
  exatos: number;
  cores_certas: number;
  numero_tentativa: number;
  status: StatusJogo;
  pontuacao: number | null;
}

export interface RespostaJogo {
  id: number;
  codigo: string;
  status: StatusJogo;
  total_tentativas: number;
  matriz_tentativas: RegistroTentativa[];
  pontuacao: number;
  iniciado_em: string;
  finalizado_em: string | null;
  duracao_segundos: number | null;
}

export interface EntradaRanking {
  posicao: number;
  nome_usuario: string;
  pontuacao: number;
  total_tentativas: number;
  duracao_segundos: number | null;
  finalizado_em: string | null;
}

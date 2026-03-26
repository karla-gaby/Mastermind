export interface RequisicaoRegistro {
  nome_usuario: string;
  email: string;
  senha: string;
}

export interface RequisicaoEntrada {
  nome_usuario: string;
  senha: string;
}

export interface RespostaToken {
  token_acesso: string;
  tipo_token: string;
  usuario_id: number;
  nome_usuario: string;
}

export interface RespostaUsuario {
  id: number;
  nome_usuario: string;
  email: string;
  criado_em: string;
}

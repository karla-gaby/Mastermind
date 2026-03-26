import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  RequisicaoEntrada,
  RequisicaoRegistro,
  RespostaToken,
  RespostaUsuario,
} from '../models/auth.model';

const CHAVE_TOKEN   = 'mm_token';
const CHAVE_USUARIO = 'mm_usuario';

@Injectable({ providedIn: 'root' })
export class ServicoAutenticacao {
  private api = `${environment.apiUrl}/auth`;

  readonly usuarioAtual = signal<{ id: number; nome_usuario: string } | null>(
    this._carregarUsuario()
  );

  constructor(private http: HttpClient, private router: Router) {}

  registrar(dados: RequisicaoRegistro): Observable<RespostaUsuario> {
    return this.http.post<RespostaUsuario>(`${this.api}/registrar`, dados);
  }

  autenticar(dados: RequisicaoEntrada): Observable<RespostaToken> {
    return this.http.post<RespostaToken>(`${this.api}/entrar`, dados).pipe(
      tap((res) => {
        localStorage.setItem(CHAVE_TOKEN, res.token_acesso);
        const usuario = { id: res.usuario_id, nome_usuario: res.nome_usuario };
        localStorage.setItem(CHAVE_USUARIO, JSON.stringify(usuario));
        this.usuarioAtual.set(usuario);
      })
    );
  }

  sair(): void {
    localStorage.removeItem(CHAVE_TOKEN);
    localStorage.removeItem(CHAVE_USUARIO);
    this.usuarioAtual.set(null);
    this.router.navigate(['/entrar']);
  }

  obterToken(): string | null {
    return localStorage.getItem(CHAVE_TOKEN);
  }

  estaAutenticado(): boolean {
    return !!this.obterToken();
  }

  private _carregarUsuario(): { id: number; nome_usuario: string } | null {
    try {
      const raw = localStorage.getItem(CHAVE_USUARIO);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }
}

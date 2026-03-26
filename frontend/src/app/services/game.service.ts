import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  RespostaInicioJogo,
  RespostaTentativa,
  RespostaJogo,
} from '../models/game.model';

@Injectable({ providedIn: 'root' })
export class ServicoJogo {
  private api = `${environment.apiUrl}/jogos`;

  constructor(private http: HttpClient) {}

  iniciarJogo(): Observable<RespostaInicioJogo> {
    return this.http.post<RespostaInicioJogo>(`${this.api}/iniciar`, {});
  }

  fazerTentativa(jogoId: number, tentativa: string[]): Observable<RespostaTentativa> {
    return this.http.post<RespostaTentativa>(
      `${this.api}/${jogoId}/tentativa`,
      { tentativa }
    );
  }

  buscarJogo(jogoId: number): Observable<RespostaJogo> {
    return this.http.get<RespostaJogo>(`${this.api}/${jogoId}`);
  }

  buscarMeusJogos(): Observable<RespostaJogo[]> {
    return this.http.get<RespostaJogo[]>(`${this.api}/`);
  }

  abandonarJogo(jogoId: number): Observable<void> {
    return this.http.post<void>(`${this.api}/${jogoId}/abandonar`, {});
  }
}

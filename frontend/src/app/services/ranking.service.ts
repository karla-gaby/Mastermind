import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { EntradaRanking } from '../models/game.model';

@Injectable({ providedIn: 'root' })
export class ServicoRanking {
  private api = `${environment.apiUrl}/ranking`;

  constructor(private http: HttpClient) {}

  buscarRanking(): Observable<EntradaRanking[]> {
    return this.http.get<EntradaRanking[]>(`${this.api}/`);
  }
}

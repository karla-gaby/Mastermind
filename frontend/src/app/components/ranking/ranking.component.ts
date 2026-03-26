import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ServicoRanking } from '../../services/ranking.service';
import { EntradaRanking } from '../../models/game.model';

@Component({
  selector: 'app-classificacao',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './ranking.component.html',
  styleUrl: './ranking.component.scss',
})
export class ClassificacaoComponent implements OnInit {
  entradas   = signal<EntradaRanking[]>([]);
  carregando = signal(true);
  erro       = signal('');

  constructor(private servicoRanking: ServicoRanking) {}

  ngOnInit(): void {
    this.servicoRanking.buscarRanking().subscribe({
      next: (dados) => { this.entradas.set(dados); this.carregando.set(false); },
      error: () => {
        this.erro.set('Não foi possível carregar o ranking.');
        this.carregando.set(false);
      },
    });
  }

  formatarDuracao(segundos: number | null): string {
    if (segundos === null) return '—';
    const m = Math.floor(segundos / 60);
    const s = Math.floor(segundos % 60);
    return m > 0 ? `${m}m ${s}s` : `${s}s`;
  }

  medalha(posicao: number): string {
    return posicao === 1 ? '🥇' : posicao === 2 ? '🥈' : posicao === 3 ? '🥉' : '';
  }
}

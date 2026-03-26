import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { ServicoAutenticacao } from '../../services/auth.service';
import { ServicoJogo } from '../../services/game.service';
import { RespostaJogo } from '../../models/game.model';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-painel',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class PainelComponent implements OnInit {
  readonly usuario  = computed(() => this.autenticacao.usuarioAtual());
  jogos             = signal<RespostaJogo[]>([]);
  carregando        = signal(false);
  erro              = signal('');

  constructor(
    readonly autenticacao: ServicoAutenticacao,
    private servicoJogo: ServicoJogo,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.carregarHistorico();
  }

  carregarHistorico(): void {
    this.carregando.set(true);
    this.servicoJogo.buscarMeusJogos().subscribe({
      next: (jogos) => { this.jogos.set(jogos); this.carregando.set(false); },
      error: () => this.carregando.set(false),
    });
  }

  iniciarNovoJogo(): void {
    this.erro.set('');
    this.servicoJogo.iniciarJogo().subscribe({
      next: (res) => this.router.navigate(['/jogo', res.jogo_id]),
      error: (e: HttpErrorResponse) =>
        this.erro.set(
          e.status === 0
            ? 'Não foi possível conectar ao servidor.'
            : (e.error?.mensagem ?? e.error?.detail ?? 'Não foi possível iniciar o jogo.')
        ),
    });
  }

  continuarJogo(jogoId: number): void {
    this.router.navigate(['/jogo', jogoId]);
  }

  cancelarJogo(jogoId: number): void {
    if (!confirm('Tem certeza que deseja cancelar este jogo? Ele será marcado como derrota.')) return;
    this.servicoJogo.abandonarJogo(jogoId).subscribe({
      next: () => this.carregarHistorico(),
      error: (e: HttpErrorResponse) =>
        this.erro.set(e.error?.mensagem ?? e.error?.detail ?? 'Não foi possível cancelar o jogo.'),
    });
  }

  get totalGanhos(): number {
    return this.jogos().filter((j) => j.status === 'ganhou').length;
  }

  get melhorPontuacao(): number {
    const pontuacoes = this.jogos().map((j) => j.pontuacao);
    return pontuacoes.length ? Math.max(...pontuacoes) : 0;
  }
  get jogoAtivo(): RespostaJogo | undefined {
    return this.jogos().find((j) => j.status === 'ativo');
  }
  traduzirStatus(status: string): string {
    const mapa: Record<string, string> = {
      ativo: 'Em andamento',
      ganhou: 'Vitória',
      perdeu: 'Derrota',
    };
    return mapa[status] ?? status;
  }
}

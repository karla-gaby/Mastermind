import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ServicoJogo } from '../../services/game.service';
import {
  RegistroTentativa,
  Cor,
  CORES,
  ROTULOS_COR,
  RespostaJogo,
  StatusJogo,
} from '../../models/game.model';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-jogo',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss',
})
export class JogoComponent implements OnInit {
  readonly CORES       = CORES;
  readonly ROTULOS_COR = ROTULOS_COR;
  readonly MAX_TENTATIVAS = 10;
  readonly TAMANHO_CODIGO = 4;

  jogoId          = signal(0);
  status          = signal<StatusJogo>('ativo');
  tentativas      = signal<RegistroTentativa[]>([]);
  totalTentativas = signal(0);
  pontuacao       = signal(0);

  chutAtual       = signal<(Cor | null)[]>([null, null, null, null]);
  slotSelecionado = signal<number>(0);

  readonly slotsComIndice = computed(() =>
    this.chutAtual().map((cor, indice) => ({ cor, indice }))
  );
  erro            = signal('');
  carregando      = signal(false);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private servicoJogo: ServicoJogo
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.jogoId.set(id);
    this.carregarJogo(id);
  }
  carregarJogo(id: number): void {
    this.servicoJogo.buscarJogo(id).subscribe({
      next: (jogo: RespostaJogo) => this.aplicarEstadoJogo(jogo),
      error: () => this.router.navigate(['/painel']),
    });
  }

  private aplicarEstadoJogo(jogo: RespostaJogo): void {
    this.status.set(jogo.status);
    this.tentativas.set(jogo.matriz_tentativas);
    this.totalTentativas.set(jogo.total_tentativas);
    this.pontuacao.set(jogo.pontuacao);
  }

  selecionarSlot(indice: number): void {
    if (this.status() !== 'ativo') return;
    this.slotSelecionado.set(indice);
  }

  selecionarCor(cor: Cor): void {
    if (this.status() !== 'ativo') return;
    const chute = [...this.chutAtual()];
    chute[this.slotSelecionado()] = cor;
    this.chutAtual.set(chute as (Cor | null)[]);
    const proximoVazio = chute.findIndex((c, i) => i > this.slotSelecionado() && c === null);
    if (proximoVazio !== -1) this.slotSelecionado.set(proximoVazio);
  }

  limparSlot(indice: number): void {
    const chute = [...this.chutAtual()];
    chute[indice] = null;
    this.chutAtual.set(chute as (Cor | null)[]);
    this.slotSelecionado.set(indice);
  }

  get chuteCompleto(): boolean {
    return this.chutAtual().every((c) => c !== null);
  }

  enviarTentativa(): void {
    if (!this.chuteCompleto || this.carregando()) return;
    this.erro.set('');
    this.carregando.set(true);

    const tentativa = this.chutAtual() as Cor[];
    this.servicoJogo.fazerTentativa(this.jogoId(), tentativa).subscribe({
      next: (res) => {
        const registro: RegistroTentativa = {
          numero_tentativa: res.numero_tentativa,
          tentativa,
          exatos: res.exatos,
          cores_certas: res.cores_certas,
        };
        this.tentativas.update((prev) => [...prev, registro]);
        this.totalTentativas.set(res.numero_tentativa);
        this.status.set(res.status);
        if (res.pontuacao !== null) this.pontuacao.set(res.pontuacao);
        this.chutAtual.set([null, null, null, null]);
        this.slotSelecionado.set(0);
        this.carregando.set(false);
      },
      error: (e: HttpErrorResponse) => {
        this.erro.set(
          e.status === 0
            ? 'Não foi possível conectar ao servidor.'
            : (e.error?.mensagem ?? e.error?.detail ?? 'Erro ao enviar tentativa.')
        );
        this.carregando.set(false);
      },
    });
  }
  irParaPainel(): void {
    this.router.navigate(['/painel']);
  }

  arrayLinhas(): number[] {
    return Array.from({ length: this.MAX_TENTATIVAS }, (_, i) => i);
  }
  buscarTentativa(indiceLinha: number): RegistroTentativa | null {
    const numeroTentativa = this.MAX_TENTATIVAS - indiceLinha;
    return this.tentativas().find((t) => t.numero_tentativa === numeroTentativa) ?? null;
  }

  ehLinhaAtual(indiceLinha: number): boolean {
    const numeroTentativa = this.MAX_TENTATIVAS - indiceLinha;
    return (
      this.status() === 'ativo' &&
      numeroTentativa === this.totalTentativas() + 1
    );
  }

  arrayPinos(n: number): number[] {
    return Array.from({ length: n });
  }
  classeCor(cor: Cor | null): string {
    return cor ? `cor-${cor}` : 'vazio';
  }
}

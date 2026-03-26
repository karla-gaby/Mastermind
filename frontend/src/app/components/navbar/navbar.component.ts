import { Component, computed } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { ServicoAutenticacao } from '../../services/auth.service';

@Component({
  selector: 'app-navegacao',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss',
})
export class NavegacaoComponent {
  readonly usuario      = computed(() => this.autenticacao.usuarioAtual());
  readonly estaLogado   = computed(() => this.autenticacao.estaAutenticado());

  constructor(readonly autenticacao: ServicoAutenticacao) {}

  sair(): void {
    this.autenticacao.sair();
  }
}

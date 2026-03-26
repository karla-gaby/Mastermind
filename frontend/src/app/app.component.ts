import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavegacaoComponent } from './components/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavegacaoComponent],
  template: `
    <app-navegacao />
    <main class="conteudo-principal">
      <router-outlet />
    </main>
  `,
  styles: [`
    .conteudo-principal {
      min-height: calc(100vh - 64px);
      padding: 2rem 1rem;
    }
  `],
})
export class AppComponent {}

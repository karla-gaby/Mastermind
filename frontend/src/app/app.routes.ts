import { Routes } from '@angular/router';
import { guardaAutenticacao } from './guards/auth.guard';

export const rotas: Routes = [
  { path: '', redirectTo: 'painel', pathMatch: 'full' },
  {
    path: 'entrar',
    loadComponent: () =>
      import('./components/login/login.component').then((m) => m.EntrarComponent),
  },
  {
    path: 'painel',
    loadComponent: () =>
      import('./components/dashboard/dashboard.component').then((m) => m.PainelComponent),
    canActivate: [guardaAutenticacao],
  },
  {
    path: 'jogo/:id',
    loadComponent: () =>
      import('./components/game/game.component').then((m) => m.JogoComponent),
    canActivate: [guardaAutenticacao],
  },
  {
    path: 'ranking',
    loadComponent: () =>
      import('./components/ranking/ranking.component').then((m) => m.ClassificacaoComponent),
    canActivate: [guardaAutenticacao],
  },
  { path: '**', redirectTo: 'painel' },
];

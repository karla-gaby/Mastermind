import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { ServicoAutenticacao } from '../services/auth.service';

export const guardaAutenticacao: CanActivateFn = () => {
  const autenticacao = inject(ServicoAutenticacao);
  if (autenticacao.estaAutenticado()) return true;
  inject(Router).navigate(['/entrar']);
  return false;
};

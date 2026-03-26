import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { ServicoAutenticacao } from './auth.service';

export const interceptorAutenticacao: HttpInterceptorFn = (req, next) => {
  const token = inject(ServicoAutenticacao).obterToken();
  if (token) {
    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }
  return next(req);
};

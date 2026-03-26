import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';

import { rotas } from './app.routes';
import { interceptorAutenticacao } from './services/auth.interceptor';

export const configuracaoApp: ApplicationConfig = {
  providers: [
    provideRouter(rotas),
    provideHttpClient(withInterceptors([interceptorAutenticacao])),
    provideAnimations(),
  ],
};

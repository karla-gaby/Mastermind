import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ServicoAutenticacao } from '../../services/auth.service';
import { HttpErrorResponse } from '@angular/common/http';

type Modo = 'entrar' | 'registrar';

@Component({
  selector: 'app-entrar',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class EntrarComponent {
  modo: Modo = 'entrar';
  erro = '';
  carregando = false;

  formularioEntrada: FormGroup;
  formularioRegistro: FormGroup;

  constructor(
    private fb: FormBuilder,
    private autenticacao: ServicoAutenticacao,
    private router: Router
  ) {
    this.formularioEntrada = this.fb.group({
      nome_usuario: ['', [Validators.required]],
      senha:        ['', [Validators.required]],
    });

    this.formularioRegistro = this.fb.group({
      nome_usuario: ['', [Validators.required, Validators.minLength(3)]],
      email:        ['', [Validators.required, Validators.email]],
      senha:        ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  alternarModo(m: Modo): void {
    this.modo = m;
    this.erro = '';
  }
  aoEntrar(): void {
    if (this.formularioEntrada.invalid) {
      this.formularioEntrada.markAllAsTouched();
      return;
    }
    this.carregando = true;
    this.erro = '';
    this.autenticacao.autenticar(this.formularioEntrada.value).subscribe({
      next: () => this.router.navigate(['/painel']),
      error: (e: HttpErrorResponse) => {
        this.erro = this._extrairMensagem(e, 'Usuário ou senha inválidos.');
        this.carregando = false;
      },
    });
  }

  aoRegistrar(): void {
    if (this.formularioRegistro.invalid) {
      this.formularioRegistro.markAllAsTouched();
      return;
    }
    this.carregando = true;
    this.erro = '';
    this.autenticacao.registrar(this.formularioRegistro.value).subscribe({
      next: () => {
        const { nome_usuario, senha } = this.formularioRegistro.value;
        this.autenticacao.autenticar({ nome_usuario, senha }).subscribe({
          next: () => this.router.navigate(['/painel']),
          error: () => {
            this.alternarModo('entrar');
            this.carregando = false;
          },
        });
      },
      error: (e: HttpErrorResponse) => {
        this.erro = this._extrairMensagem(e, 'Falha ao criar conta.');
        this.carregando = false;
      },
    });
  }

  erroCampo(form: FormGroup, campo: string, regra: string): boolean {
    const c = form.get(campo);
    return !!(c?.hasError(regra) && c.touched);
  }

  private _extrairMensagem(e: HttpErrorResponse, fallback: string): string {
    if (e.status === 0) {
      return 'Não foi possível conectar ao servidor. Verifique se o backend está rodando na porta 8000.';
    }
    return e.error?.mensagem ?? e.error?.detail ?? fallback;
  }
}

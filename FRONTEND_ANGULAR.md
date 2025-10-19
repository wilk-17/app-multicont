# 🅰️ Frontend Angular - Multicont App

## 📋 Tabla de Contenidos

1. [Información General](#información-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Autenticación JWT](#autenticación-jwt)
6. [Servicios y API](#servicios-y-api)
7. [Componentes Principales](#componentes-principales)
8. [Rutas y Navegación](#rutas-y-navegación)
9. [Guards y Seguridad](#guards-y-seguridad)
10. [Despliegue](#despliegue)

---

## 📱 Información General

**Sistema de Gestión Empresarial - Frontend Angular**

- **Framework**: Angular 17+ (Standalone Components)
- **UI Library**: Angular Material / PrimeNG
- **State Management**: RxJS + Services
- **HTTP Client**: Angular HttpClient con Interceptors
- **Autenticación**: JWT (JSON Web Tokens)
- **Charts**: Chart.js / ng2-charts / ApexCharts
- **Formularios**: Reactive Forms
- **Estilos**: SCSS + Tailwind CSS

### Funcionalidades Principales

- ✅ Sistema de autenticación con JWT
- ✅ Dashboard con métricas y KPIs
- ✅ Gestión de organizaciones y sucursales
- ✅ Administración de empleados
- ✅ Control de inventario
- ✅ Cotizaciones y órdenes de venta
- ✅ Facturación
- ✅ Reportes y analytics
- ✅ Metas de ventas (mensuales, trimestrales, anuales)

---

## 🔧 Requisitos Previos

### Software Necesario

```bash
# Node.js (LTS - versión 18 o superior)
node --version  # v18.x.x o superior

# npm (viene con Node.js)
npm --version   # 9.x.x o superior

# Angular CLI
npm install -g @angular/cli@latest

# Verificar instalación de Angular
ng version
```

### Backend

- ✅ Flask API corriendo en `http://127.0.0.1:5000`
- ✅ Swagger docs en `http://127.0.0.1:5000/api/docs/`
- ✅ Sistema de autenticación JWT activado
- ✅ Base de datos poblada con datos de prueba

---

## 🚀 Instalación y Configuración

### 1. Crear Proyecto Angular

```bash
# Crear nuevo proyecto con standalone components
ng new frontend-multicont --standalone --style=scss --routing

# Responder a las preguntas:
# ? Would you like to enable Server-Side Rendering (SSR)? No
# ? Would you like to add Angular Material? Yes

cd frontend-multicont
```

### 2. Instalar Dependencias

```bash
# Angular Material (si no se instaló antes)
ng add @angular/material

# PrimeNG (alternativa a Material - escoger uno)
npm install primeng primeicons

# Chart.js para gráficos
npm install chart.js ng2-charts

# JWT Decode
npm install jwt-decode

# Date-fns para manejo de fechas
npm install date-fns

# Tailwind CSS (opcional)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

### 3. Configurar Tailwind (Opcional)

**tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**src/styles.scss:**
```scss
@tailwind base;
@tailwind components;
@tailwind utilities;

// Angular Material theme
@import '@angular/material/prebuilt-themes/indigo-pink.css';
```

### 4. Configurar Environment

**src/environments/environment.ts:**
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:5000/api',
  apiTimeout: 30000
};
```

**src/environments/environment.prod.ts:**
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://tu-dominio.com/api',
  apiTimeout: 30000
};
```

---

## 📁 Estructura del Proyecto

```
frontend-multicont/
├── src/
│   ├── app/
│   │   ├── core/                      # Servicios globales y configuración
│   │   │   ├── guards/
│   │   │   │   ├── auth.guard.ts
│   │   │   │   └── role.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── auth.interceptor.ts
│   │   │   │   └── error.interceptor.ts
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── api.service.ts
│   │   │   │   └── storage.service.ts
│   │   │   └── models/
│   │   │       ├── user.model.ts
│   │   │       ├── auth.model.ts
│   │   │       └── api-response.model.ts
│   │   │
│   │   ├── features/                  # Módulos funcionales
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   └── login.component.ts
│   │   │   │   └── auth.routes.ts
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── dashboard.component.ts
│   │   │   │   ├── widgets/
│   │   │   │   └── dashboard.routes.ts
│   │   │   │
│   │   │   ├── organizations/
│   │   │   │   ├── organization-list/
│   │   │   │   ├── organization-detail/
│   │   │   │   ├── organization-form/
│   │   │   │   └── organizations.routes.ts
│   │   │   │
│   │   │   ├── branches/
│   │   │   ├── employees/
│   │   │   ├── inventory/
│   │   │   ├── quotes/
│   │   │   ├── sales-orders/
│   │   │   ├── invoices/
│   │   │   ├── sales-goals/
│   │   │   └── analytics/
│   │   │
│   │   ├── shared/                    # Componentes reutilizables
│   │   │   ├── components/
│   │   │   │   ├── navbar/
│   │   │   │   ├── sidebar/
│   │   │   │   ├── loading-spinner/
│   │   │   │   ├── data-table/
│   │   │   │   └── confirm-dialog/
│   │   │   ├── directives/
│   │   │   └── pipes/
│   │   │       ├── currency-cop.pipe.ts
│   │   │       └── date-format.pipe.ts
│   │   │
│   │   ├── app.component.ts
│   │   ├── app.config.ts
│   │   └── app.routes.ts
│   │
│   ├── assets/
│   ├── styles.scss
│   └── index.html
│
├── angular.json
├── package.json
└── tsconfig.json
```

---

## 🔐 Autenticación JWT

### 1. Auth Service

**src/app/core/services/auth.service.ts:**
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { jwtDecode } from 'jwt-decode';
import { environment } from '../../../environments/environment';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: {
    id: number;
    username: string;
    role: string;
    role_id: number;
    permissions: string[];
  };
}

export interface DecodedToken {
  sub: number;
  role: string;
  role_id: number;
  permissions: string[];
  exp: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  
  private currentUserSubject = new BehaviorSubject<any>(this.getUserFromToken());
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private readonly TOKEN_KEY = 'access_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';
  
  constructor() {}
  
  login(credentials: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${environment.apiUrl}/auth/login`, credentials)
      .pipe(
        tap(response => {
          this.setTokens(response.access_token, response.refresh_token);
          this.currentUserSubject.next(response.user);
        })
      );
  }
  
  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }
  
  refreshToken(): Observable<{ access_token: string }> {
    const refreshToken = this.getRefreshToken();
    return this.http.post<{ access_token: string }>(
      `${environment.apiUrl}/auth/refresh`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${refreshToken}`
        }
      }
    ).pipe(
      tap(response => {
        localStorage.setItem(this.TOKEN_KEY, response.access_token);
      })
    );
  }
  
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }
  
  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }
  
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;
    
    try {
      const decoded: DecodedToken = jwtDecode(token);
      return decoded.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }
  
  hasRole(role: string): boolean {
    const user = this.currentUserSubject.value;
    return user?.role === role;
  }
  
  hasPermission(permission: string): boolean {
    const user = this.currentUserSubject.value;
    return user?.permissions?.includes(permission) || false;
  }
  
  private setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.TOKEN_KEY, accessToken);
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
  }
  
  private getUserFromToken(): any {
    const token = this.getToken();
    if (!token) return null;
    
    try {
      const decoded: DecodedToken = jwtDecode(token);
      return {
        id: decoded.sub,
        role: decoded.role,
        role_id: decoded.role_id,
        permissions: decoded.permissions
      };
    } catch {
      return null;
    }
  }
}
```

### 2. Auth Interceptor

**src/app/core/interceptors/auth.interceptor.ts:**
```typescript
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();
  
  if (token && !req.url.includes('/auth/login')) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }
  
  return next(req);
};
```

### 3. Error Interceptor

**src/app/core/interceptors/error.interceptor.ts:**
```typescript
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const authService = inject(AuthService);
  
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Token expirado o inválido
        authService.logout();
        router.navigate(['/login']);
      }
      
      if (error.status === 403) {
        // Sin permisos
        router.navigate(['/unauthorized']);
      }
      
      return throwError(() => error);
    })
  );
};
```

### 4. Auth Guard

**src/app/core/guards/auth.guard.ts:**
```typescript
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  if (authService.isAuthenticated()) {
    return true;
  }
  
  router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
  return false;
};
```

### 5. Role Guard

**src/app/core/guards/role.guard.ts:**
```typescript
import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard: (roles: string[]) => CanActivateFn = (roles: string[]) => {
  return (route, state) => {
    const authService = inject(AuthService);
    const router = inject(Router);
    
    if (!authService.isAuthenticated()) {
      router.navigate(['/login']);
      return false;
    }
    
    const hasRole = roles.some(role => authService.hasRole(role));
    
    if (hasRole) {
      return true;
    }
    
    router.navigate(['/unauthorized']);
    return false;
  };
};
```

### 6. Login Component

**src/app/features/auth/login/login.component.ts:**
```typescript
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule
  ],
  template: `
    <div class="login-container">
      <mat-card class="login-card">
        <mat-card-header>
          <mat-card-title>Multicont App</mat-card-title>
          <mat-card-subtitle>Iniciar Sesión</mat-card-subtitle>
        </mat-card-header>
        
        <mat-card-content>
          <form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Usuario</mat-label>
              <input matInput formControlName="username" autocomplete="username">
              @if (loginForm.get('username')?.hasError('required')) {
                <mat-error>Usuario es requerido</mat-error>
              }
            </mat-form-field>
            
            <mat-form-field appearance="outline" class="full-width">
              <mat-label>Contraseña</mat-label>
              <input matInput type="password" formControlName="password" autocomplete="current-password">
              @if (loginForm.get('password')?.hasError('required')) {
                <mat-error>Contraseña es requerida</mat-error>
              }
            </mat-form-field>
            
            @if (errorMessage) {
              <div class="error-message">{{ errorMessage }}</div>
            }
            
            <button mat-raised-button color="primary" type="submit" 
                    [disabled]="loginForm.invalid || loading" class="full-width">
              @if (loading) {
                <mat-spinner diameter="20"></mat-spinner>
              } @else {
                Ingresar
              }
            </button>
          </form>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .login-card {
      width: 100%;
      max-width: 400px;
      padding: 2rem;
    }
    
    .full-width {
      width: 100%;
      margin-bottom: 1rem;
    }
    
    .error-message {
      color: #f44336;
      margin-bottom: 1rem;
      padding: 0.5rem;
      background: #ffebee;
      border-radius: 4px;
      text-align: center;
    }
    
    mat-spinner {
      margin: 0 auto;
    }
  `]
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  
  loginForm = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });
  
  loading = false;
  errorMessage = '';
  
  onSubmit(): void {
    if (this.loginForm.invalid) return;
    
    this.loading = true;
    this.errorMessage = '';
    
    this.authService.login(this.loginForm.value as any).subscribe({
      next: () => {
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        this.errorMessage = 'Usuario o contraseña incorrectos';
        this.loading = false;
      }
    });
  }
}
```

---

## 🌐 Servicios y API

### API Service Base

**src/app/core/services/api.service.ts:**
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = environment.apiUrl;
  
  get<T>(endpoint: string, params?: any): Observable<ApiResponse<T>> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    
    return this.http.get<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`, { params: httpParams });
  }
  
  post<T>(endpoint: string, data: any): Observable<ApiResponse<T>> {
    return this.http.post<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`, data);
  }
  
  put<T>(endpoint: string, data: any): Observable<ApiResponse<T>> {
    return this.http.put<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`, data);
  }
  
  delete<T>(endpoint: string): Observable<ApiResponse<T>> {
    return this.http.delete<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`);
  }
}
```

### Example: Organization Service

**src/app/features/organizations/services/organization.service.ts:**
```typescript
import { Injectable, inject } from '@angular/core';
import { Observable, map } from 'rxjs';
import { ApiService, ApiResponse, PaginatedResponse } from '../../../core/services/api.service';

export interface Organization {
  id: string;
  historical_name: string;
  current_name: string;
}

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  private apiService = inject(ApiService);
  
  getAll(page: number = 1, per_page: number = 10): Observable<PaginatedResponse<Organization>> {
    return this.apiService.get<PaginatedResponse<Organization>>('organizations', { page, per_page })
      .pipe(map(response => response.data!));
  }
  
  getById(id: string): Observable<Organization> {
    return this.apiService.get<Organization>(`organizations/${id}`)
      .pipe(map(response => response.data!));
  }
  
  create(data: Partial<Organization>): Observable<Organization> {
    return this.apiService.post<Organization>('organizations', data)
      .pipe(map(response => response.data!));
  }
  
  update(id: string, data: Partial<Organization>): Observable<Organization> {
    return this.apiService.put<Organization>(`organizations/${id}`, data)
      .pipe(map(response => response.data!));
  }
  
  delete(id: string): Observable<void> {
    return this.apiService.delete<void>(`organizations/${id}`)
      .pipe(map(() => undefined));
  }
}
```

---

## 🛤️ Rutas y Configuración

### App Routes

**src/app/app.routes.ts:**
```typescript
import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component')
      .then(m => m.LoginComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component')
      .then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: 'organizations',
    loadChildren: () => import('./features/organizations/organizations.routes')
      .then(m => m.organizationsRoutes),
    canActivate: [authGuard, roleGuard(['ADMIN', 'MANAGER'])]
  },
  {
    path: 'analytics',
    loadChildren: () => import('./features/analytics/analytics.routes')
      .then(m => m.analyticsRoutes),
    canActivate: [authGuard]
  },
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
```

### App Config

**src/app/app.config.ts:**
```typescript
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { routes } from './app.routes';
import { authInterceptor } from './core/interceptors/auth.interceptor';
import { errorInterceptor } from './core/interceptors/error.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(
      withInterceptors([authInterceptor, errorInterceptor])
    ),
    provideAnimations()
  ]
};
```

---

## 🎨 Componentes Principales

### Dashboard Component

Ver ejemplo completo en el archivo generado con ng generate

### Data Table Component

Componente reutilizable para listar datos con paginación, filtros y acciones

---

## 🚀 Comandos de Desarrollo

```bash
# Desarrollo
ng serve                    # http://localhost:4200
ng serve --open            # Abre automáticamente en navegador
ng serve --port 4300       # Especificar puerto

# Build
ng build                   # Desarrollo
ng build --configuration production  # Producción

# Testing
ng test                    # Unit tests
ng e2e                     # End-to-end tests

# Generar componentes
ng generate component features/dashboard
ng generate service core/services/api

# Análisis de bundle
ng build --stats-json
npx webpack-bundle-analyzer dist/frontend-multicont/stats.json
```

---

## 📦 Despliegue

### Build para Producción

```bash
# Build optimizado
ng build --configuration production

# Los archivos estarán en dist/frontend-multicont/
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    root /var/www/frontend-multicont/dist/browser;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📚 Recursos Adicionales

- [Angular Documentation](https://angular.dev)
- [Angular Material](https://material.angular.io/)
- [PrimeNG](https://primeng.org/)
- [RxJS](https://rxjs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## ✅ Checklist de Implementación

- [ ] Crear proyecto Angular
- [ ] Configurar environments
- [ ] Instalar dependencias (Material/PrimeNG)
- [ ] Implementar AuthService
- [ ] Crear interceptors (Auth + Error)
- [ ] Implementar guards (Auth + Role)
- [ ] Componente de Login
- [ ] Layout principal (Navbar + Sidebar)
- [ ] Dashboard con widgets
- [ ] Servicios para cada módulo
- [ ] Componentes CRUD para cada entidad
- [ ] Gráficos y reportes
- [ ] Testing
- [ ] Build y despliegue

---

**🎉 ¡Listo para desarrollar el frontend en Angular!**

Usa los ejemplos de código proporcionados como base y personalízalos según las necesidades específicas del proyecto.

# ROADMAP DE IMPLEMENTACIÓN - ITEMS PENDIENTES
## Proyecto: multiCont - Sistema de Gestión de Ventas

---

## 📊 ESTADO ACTUAL DEL PROYECTO

```
COMPLETADO: ██████████████████░░░░░░░░░░ 60%

Backend API:     ████████████████████████ 100% ✅
Frontend:        ░░░░░░░░░░░░░░░░░░░░░░░░   0% ❌
Autenticación:   ░░░░░░░░░░░░░░░░░░░░░░░░   0% ❌
```

---

## 🎯 ITEMS SEGÚN IMAGEN DEL REQUERIMIENTO

### ✅ COMPLETADOS

1. **✅ ORM (Object-Relational Mapping)**
   - SQLAlchemy implementado
   - 21 entidades mapeadas
   - Relaciones FK configuradas
   - Migraciones funcionando

2. **✅ Controladores (Validados)**
   - 21 handlers con lógica de negocio
   - Validaciones de campos
   - Validaciones de unicidad
   - Manejo de errores

3. **✅ Paginación**
   - Implementada en todos los endpoints
   - Parámetros: `?page=1&per_page=10`
   - Metadatos de paginación en respuesta

4. **✅ Alcance del Negocio (Backend)**
   - Sistema de metas de ventas
   - Tracking de facturación
   - Análisis por marca
   - Flujo Quote → Order → Invoice

5. **✅ Reportes de Aplicación (Backend)**
   - API de Analytics completa
   - 7 endpoints especializados
   - Metas vs facturación real
   - Top performers

---

### ⚠️ PARCIALMENTE COMPLETADOS

6. **⚠️ Interfaces de CRUD por tabla (Dashboard/Admin Panel)**
   - ✅ Backend: 21 APIs REST funcionando
   - ❌ Frontend: Sin implementar

7. **⚠️ Configuración Funcional**
   - ✅ CRUD de usuarios, roles, permisos
   - ❌ Sin middleware de autorización
   - ❌ Sin panel de configuración visual

---

### ❌ PENDIENTES (CRÍTICOS)

8. **❌ Usuarios - Permisos (Sistema de Autenticación)**
   - ❌ Login/Logout
   - ❌ Tokens JWT
   - ❌ Hash de contraseñas
   - ❌ Protección de endpoints

9. **❌ Módulos/Configuración Técnica**
   - ❌ Logs de auditoría
   - ❌ Configuración del sistema
   - ❌ Backup/Restore

10. **❌ Frontend Completo**
    - ❌ Dashboard visual
    - ❌ Formularios CRUD
    - ❌ Gráficos de reportes
    - ❌ Tablas interactivas

---

## 📅 PLAN DE IMPLEMENTACIÓN (8-10 DÍAS)

### 🔴 DÍA 1: SEGURIDAD - AUTENTICACIÓN JWT
**Prioridad: CRÍTICA**

**Tareas:**
```bash
# 1. Instalar dependencias
pip install flask-jwt-extended werkzeug python-jose

# 2. Archivos a crear/modificar
app/
├── api/
│   └── auth_api.py          # ← NUEVO: endpoints de login/logout
├── utils/
│   ├── __init__.py          # ← NUEVO
│   ├── security.py          # ← NUEVO: hash passwords, JWT
│   └── decorators.py        # ← NUEVO: @require_role, @require_permission
└── use_cases/
    └── user_handler.py      # ← MODIFICAR: hashear passwords
```

**Endpoints a crear:**
- `POST /api/auth/login` - Login y obtener token
- `POST /api/auth/logout` - Invalidar token
- `POST /api/auth/refresh` - Renovar token
- `GET /api/auth/me` - Info del usuario logueado

**Resultado esperado:**
```bash
# Hacer login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"ana","password":"ana123"}'

# Respuesta
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "ana",
    "role": "SALES"
  }
}

# Usar token en otros endpoints
curl -X GET http://localhost:5000/api/sales_goals/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Checklist Día 1:**
- [ ] Crear `auth_api.py` con login/logout
- [ ] Implementar hash de passwords en `user_handler.py`
- [ ] Crear decoradores `@jwt_required()` y `@require_role()`
- [ ] Proteger endpoints críticos (sales_goals, users)
- [ ] Actualizar contraseñas existentes en BD con hash
- [ ] Probar login y acceso a endpoints protegidos

---

### 🟢 DÍA 2-3: FRONTEND - ESTRUCTURA BASE
**Prioridad: ALTA**

**Tecnología elegida: Vue.js 3 + Vite**

**Día 2: Setup del proyecto**
```bash
# Crear proyecto Vue
npm create vite@latest frontend -- --template vue

cd frontend
npm install vue-router pinia axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Estructura de carpetas:**
```
frontend/
├── src/
│   ├── assets/           # Estilos, imágenes
│   ├── components/       # Componentes reutilizables
│   │   ├── Navbar.vue
│   │   ├── Sidebar.vue
│   │   ├── DataTable.vue
│   │   └── FormModal.vue
│   ├── views/            # Vistas principales
│   │   ├── Login.vue
│   │   ├── Dashboard.vue
│   │   ├── Users/
│   │   │   ├── UserList.vue
│   │   │   └── UserForm.vue
│   │   └── Sales/
│   │       ├── QuoteList.vue
│   │       └── Goals.vue
│   ├── router/
│   │   └── index.js      # Rutas de la app
│   ├── stores/
│   │   ├── auth.js       # Store de autenticación
│   │   └── users.js      # Store de usuarios
│   ├── services/
│   │   └── api.js        # Cliente HTTP (Axios)
│   ├── App.vue
│   └── main.js
├── package.json
└── vite.config.js
```

**Día 3: Implementar Login**

**`src/views/Login.vue`:**
```vue
<template>
  <div class="login-container">
    <div class="login-card">
      <h1>multiCont</h1>
      <form @submit.prevent="handleLogin">
        <input v-model="username" placeholder="Usuario" />
        <input v-model="password" type="password" placeholder="Contraseña" />
        <button type="submit">Iniciar Sesión</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleLogin() {
  try {
    await authStore.login(username.value, password.value)
    router.push('/dashboard')
  } catch (err) {
    error.value = 'Credenciales inválidas'
  }
}
</script>
```

**`src/stores/auth.js`:**
```javascript
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),

  actions: {
    async login(username, password) {
      const response = await axios.post('/api/auth/login', { username, password })
      this.token = response.data.access_token
      this.user = response.data.user
      localStorage.setItem('token', this.token)
      
      // Configurar token en Axios para futuras requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
```

**Checklist Día 2-3:**
- [ ] Crear proyecto Vue.js con Vite
- [ ] Instalar dependencias (vue-router, pinia, axios)
- [ ] Configurar Tailwind CSS
- [ ] Crear store de autenticación
- [ ] Implementar vista de Login
- [ ] Configurar router con rutas protegidas
- [ ] Crear layout base (Sidebar + Navbar)
- [ ] Probar login y navegación

---

### 🟢 DÍA 4-5: FRONTEND - CRUD DE USUARIOS Y BRANDS
**Prioridad: ALTA**

**Día 4: Vista de Usuarios**

**Componentes a crear:**

1. **`UserList.vue`** - Lista de usuarios con tabla
```vue
<template>
  <div class="user-list">
    <div class="header">
      <h1>Usuarios</h1>
      <button @click="showCreateModal = true">Crear Usuario</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Persona</th>
          <th>Rol</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.person_name }}</td>
          <td>{{ user.role_name }}</td>
          <td>
            <button @click="editUser(user)">Editar</button>
            <button @click="deleteUser(user.id)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Paginación -->
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
      <span>Página {{ currentPage }} de {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
    </div>

    <!-- Modal de creación/edición -->
    <UserFormModal
      v-if="showCreateModal"
      :user="selectedUser"
      @close="showCreateModal = false"
      @saved="loadUsers"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import UserFormModal from './UserFormModal.vue'

const users = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const showCreateModal = ref(false)
const selectedUser = ref(null)

async function loadUsers() {
  const response = await axios.get(`/api/users/?page=${currentPage.value}&per_page=10`)
  users.value = response.data.data.items
  totalPages.value = response.data.data.total_pages
}

function editUser(user) {
  selectedUser.value = user
  showCreateModal.value = true
}

async function deleteUser(id) {
  if (confirm('¿Eliminar este usuario?')) {
    await axios.delete(`/api/users/${id}`)
    loadUsers()
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    loadUsers()
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    loadUsers()
  }
}

onMounted(() => {
  loadUsers()
})
</script>
```

2. **`UserFormModal.vue`** - Modal de creación/edición
```vue
<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <h2>{{ user ? 'Editar Usuario' : 'Crear Usuario' }}</h2>
      
      <form @submit.prevent="save">
        <div class="form-group">
          <label>Username</label>
          <input v-model="form.username" required />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" :required="!user" />
        </div>

        <div class="form-group">
          <label>Persona</label>
          <select v-model="form.person_id" required>
            <option value="">Seleccione...</option>
            <option v-for="person in persons" :key="person.id" :value="person.id">
              {{ person.first_name }} {{ person.last_name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Rol</label>
          <select v-model="form.role_id" required>
            <option value="">Seleccione...</option>
            <option v-for="role in roles" :key="role.id" :value="role.id">
              {{ role.name }}
            </option>
          </select>
        </div>

        <div class="form-actions">
          <button type="button" @click="$emit('close')">Cancelar</button>
          <button type="submit">Guardar</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps(['user'])
const emit = defineEmits(['close', 'saved'])

const form = ref({
  username: '',
  password: '',
  person_id: null,
  role_id: null
})

const persons = ref([])
const roles = ref([])

async function loadData() {
  const [personsRes, rolesRes] = await Promise.all([
    axios.get('/api/persons/?per_page=100'),
    axios.get('/api/roles/?per_page=100')
  ])
  
  persons.value = personsRes.data.data.items
  roles.value = rolesRes.data.data.items

  if (props.user) {
    form.value = { ...props.user }
  }
}

async function save() {
  try {
    if (props.user) {
      await axios.put(`/api/users/${props.user.id}`, form.value)
    } else {
      await axios.post('/api/users/', form.value)
    }
    emit('saved')
    emit('close')
  } catch (error) {
    alert('Error al guardar: ' + error.response?.data?.error)
  }
}

onMounted(() => {
  loadData()
})
</script>
```

**Día 5: Vista de Brands (más simple)**

Similar a usuarios pero con solo 2 campos (name, description).

**Checklist Día 4-5:**
- [ ] Crear componente `UserList.vue`
- [ ] Crear componente `UserFormModal.vue`
- [ ] Implementar tabla con paginación
- [ ] Implementar CRUD completo (crear, editar, eliminar)
- [ ] Crear vista de Brands similar
- [ ] Agregar estilos con Tailwind
- [ ] Probar flujo completo de CRUD

---

### 🟡 DÍA 6-7: FRONTEND - DASHBOARD CON KPIS
**Prioridad: MEDIA**

**Librerías a instalar:**
```bash
npm install chart.js vue-chartjs
```

**Vista de Dashboard:**

**`Dashboard.vue`:**
```vue
<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <!-- KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <h3>Total Facturado</h3>
        <p class="kpi-value">${{ formatNumber(kpis.total_invoiced) }}</p>
        <span class="kpi-period">Octubre 2025</span>
      </div>

      <div class="kpi-card">
        <h3>Facturas</h3>
        <p class="kpi-value">{{ kpis.invoice_count }}</p>
      </div>

      <div class="kpi-card">
        <h3>Cotizaciones</h3>
        <p class="kpi-value">{{ kpis.quote_count }}</p>
      </div>

      <div class="kpi-card">
        <h3>Vendedores Activos</h3>
        <p class="kpi-value">{{ kpis.active_employees }}</p>
      </div>
    </div>

    <!-- Gráfico de ventas por empleado -->
    <div class="chart-container">
      <h2>Top 5 Vendedores</h2>
      <Bar :data="chartData" :options="chartOptions" />
    </div>

    <!-- Tabla de metas -->
    <div class="goals-section">
      <h2>Metas del Mes</h2>
      <table>
        <thead>
          <tr>
            <th>Vendedor/Sucursal</th>
            <th>Meta</th>
            <th>Real</th>
            <th>% Logro</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="goal in goals" :key="goal.goal_id">
            <td>{{ goal.scope_name }}</td>
            <td>${{ formatNumber(goal.target_amount) }}</td>
            <td>${{ formatNumber(goal.actual_amount) }}</td>
            <td>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: goal.achievement_percentage + '%' }"
                  :class="getStatusClass(goal.status)"
                ></div>
                <span>{{ goal.achievement_percentage }}%</span>
              </div>
            </td>
            <td>
              <span :class="'badge-' + goal.status">
                {{ getStatusLabel(goal.status) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import axios from 'axios'

Chart.register(...registerables)

const kpis = ref({})
const goals = ref([])
const chartData = ref({})
const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: { display: false }
  }
})

async function loadDashboard() {
  const today = new Date()
  const startDate = `${today.getFullYear()}-${today.getMonth() + 1}-01`
  const endDate = today.toISOString().split('T')[0]

  // Cargar KPIs
  const kpisRes = await axios.get('/api/analytics/sales/summary', {
    params: { start_date: startDate, end_date: endDate }
  })
  kpis.value = kpisRes.data.data

  // Cargar top performers
  const topRes = await axios.get('/api/analytics/top_performers', {
    params: { start_date: startDate, end_date: endDate, limit: 5 }
  })
  
  const topPerformers = topRes.data.data
  chartData.value = {
    labels: topPerformers.map(p => p.employee_name),
    datasets: [{
      label: 'Facturación',
      data: topPerformers.map(p => p.total_invoiced),
      backgroundColor: 'rgba(54, 162, 235, 0.5)'
    }]
  }

  // Cargar metas vs reales
  const goalsRes = await axios.get('/api/analytics/goals/vs_actual', {
    params: { period_type: 'monthly' }
  })
  goals.value = goalsRes.data.data
}

function formatNumber(num) {
  return new Intl.NumberFormat('es-CO').format(num)
}

function getStatusClass(status) {
  const classes = {
    exceeded: 'bg-green-500',
    on_track: 'bg-blue-500',
    at_risk: 'bg-yellow-500',
    failed: 'bg-red-500'
  }
  return classes[status] || ''
}

function getStatusLabel(status) {
  const labels = {
    exceeded: 'Superada',
    on_track: 'En curso',
    at_risk: 'En riesgo',
    failed: 'No cumplida'
  }
  return labels[status] || status
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.kpi-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2563eb;
  margin: 0.5rem 0;
}

.progress-bar {
  position: relative;
  height: 24px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.badge-exceeded { color: #10b981; }
.badge-on_track { color: #3b82f6; }
.badge-at_risk { color: #f59e0b; }
.badge-failed { color: #ef4444; }
</style>
```

**Checklist Día 6-7:**
- [ ] Instalar Chart.js y vue-chartjs
- [ ] Crear componente Dashboard.vue
- [ ] Implementar tarjetas de KPIs
- [ ] Crear gráfico de top vendedores
- [ ] Crear tabla de metas con barra de progreso
- [ ] Conectar con endpoints de analytics
- [ ] Agregar estilos y animaciones
- [ ] Probar visualización de datos

---

### 🟡 DÍA 8: PULIDO Y TESTING
**Prioridad: MEDIA**

**Tareas finales:**
- [ ] Probar todos los flujos (login, CRUD, dashboard)
- [ ] Agregar mensajes de error/éxito (toasts)
- [ ] Validaciones de formularios en frontend
- [ ] Agregar loading spinners
- [ ] Responsive design para móviles
- [ ] Documentar código
- [ ] Crear README del frontend
- [ ] Deploy de prueba

---

## 📝 RESUMEN EJECUTIVO

### Lo que tienes (60%):
✅ Backend API 100% funcional  
✅ Base de datos poblada  
✅ Swagger documentation  
✅ Sistema de analytics completo  

### Lo que necesitas para el corte (40%):
❌ Autenticación JWT (1 día)  
❌ Frontend básico con login (2 días)  
❌ CRUD de usuarios y brands (2 días)  
❌ Dashboard con KPIs (2 días)  
❌ Testing y pulido (1 día)  

**Total: 8 días de trabajo intensivo**

---

## 🎯 SIGUIENTE ACCIÓN INMEDIATA

**EMPEZAR AHORA CON:**

```bash
# 1. Instalar dependencias de autenticación
pip install flask-jwt-extended werkzeug

# 2. Crear archivo de autenticación
touch app/api/auth_api.py

# 3. Modificar user_handler para hash de passwords
code app/use_cases/user_handler.py
```

¿Quieres que te ayude a implementar la **FASE 1 (Autenticación JWT)** ahora mismo?

---

**Generado por:** GitHub Copilot  
**Fecha:** 2025-10-18  
**Prioridad:** 🔴 CRÍTICA  

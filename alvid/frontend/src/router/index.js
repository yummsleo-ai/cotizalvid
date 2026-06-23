import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth'
import CotizacionesView from '../views/CotizacionesView.vue'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import MaterialesView from '../views/MaterialesView.vue'
import NuevaCotizacionView from '../views/NuevaCotizacionView.vue'
import PlanCortesView from '../views/PlanCortesView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: LoginView },
    { path: '/', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/cotizaciones', name: 'cotizaciones', component: CotizacionesView, meta: { requiresAuth: true } },
    { path: '/cotizaciones/nueva', name: 'nueva-cotizacion', component: NuevaCotizacionView, meta: { requiresAuth: true } },
    { path: '/cortes', name: 'cortes', component: PlanCortesView, meta: { requiresAuth: true } },
    { path: '/materiales', name: 'materiales', component: MaterialesView, meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView, meta: { requiresAuth: true } }
  ]
})

// Protege la aplicacion cuando no existe token local.
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.autenticado) {
    return { name: 'login' }
  }
  if (to.name === 'login' && auth.autenticado) {
    return { name: 'dashboard' }
  }
  return true
})

export default router

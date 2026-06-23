<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Boxes,
  ChevronRight,
  ClipboardList,
  LayoutDashboard,
  LogOut,
  Menu,
  PlusCircle,
  Ruler,
  X
} from '@lucide/vue'

import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const menuAbierto = ref(false)

const navegacion = [
  { nombre: 'Inicio', descripcion: 'Resumen del negocio', ruta: '/', icono: LayoutDashboard },
  { nombre: 'Cotizaciones', descripcion: 'Clientes y trabajos', ruta: '/cotizaciones', icono: ClipboardList },
  { nombre: 'Nueva cotización', descripcion: 'Crear presupuesto', ruta: '/cotizaciones/nueva', icono: PlusCircle },
  { nombre: 'Plan de cortes', descripcion: 'Optimizar tableros', ruta: '/cortes', icono: Ruler },
  { nombre: 'Materiales', descripcion: 'Stock e inventario', ruta: '/materiales', icono: Boxes }
]

const tituloActual = computed(() => navegacion.find((item) => item.ruta === route.path)?.nombre || 'ALVID')
const iniciales = computed(() => (auth.usuario?.nombre || 'Usuario').split(' ').slice(0, 2).map((parte) => parte[0]).join('').toUpperCase())

function cerrarMenu() {
  menuAbierto.value = false
}

function salir() {
  auth.logout()
  cerrarMenu()
  router.push({ name: 'login' })
}
</script>

<template>
  <header class="no-print fixed inset-x-0 top-0 z-40 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur lg:hidden">
    <button class="icon-button" type="button" :aria-label="menuAbierto ? 'Cerrar menú' : 'Abrir menú'" @click="menuAbierto = !menuAbierto">
      <X v-if="menuAbierto" :size="20" />
      <Menu v-else :size="20" />
    </button>
    <div class="flex items-center gap-2">
      <span class="flex h-10 w-10 items-center justify-center rounded-lg bg-white p-0.5">
        <img src="/logo-alvid.png" alt="" class="h-full w-full object-contain" />
      </span>
      <span class="font-black text-alvid">{{ tituloActual }}</span>
    </div>
    <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-alvid-50 text-xs font-black text-alvid">{{ iniciales }}</div>
  </header>

  <div v-if="menuAbierto" class="no-print fixed inset-0 z-40 bg-slate-950/30 backdrop-blur-sm lg:hidden" @click="cerrarMenu" />

  <aside
    class="no-print fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-slate-200 bg-white transition-transform duration-300 lg:translate-x-0"
    :class="menuAbierto ? 'translate-x-0' : '-translate-x-full'"
  >
    <div class="flex h-20 items-center gap-3 border-b border-slate-100 px-5">
      <span class="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-white p-1 shadow-sm">
        <img src="/logo-alvid.png" alt="Logo ALVID" class="h-full w-full object-contain" />
      </span>
      <div>
        <p class="text-xl font-black text-alvid">ALVID</p>
        <p class="text-xs font-semibold text-slate-500">Gestión de carpintería</p>
      </div>
    </div>

    <nav class="flex-1 space-y-1 overflow-y-auto px-3 py-5" aria-label="Navegación principal">
      <p class="px-3 pb-2 text-xs font-bold uppercase text-slate-400">Operación</p>
      <RouterLink
        v-for="item in navegacion"
        :key="item.ruta"
        :to="item.ruta"
        class="group flex items-center gap-3 rounded-xl px-3 py-3 text-slate-600 transition-all hover:bg-slate-50 hover:text-slate-950"
        active-class="bg-alvid-50 text-alvid shadow-sm"
        @click="cerrarMenu"
      >
        <component :is="item.icono" :size="20" class="shrink-0" />
        <span class="min-w-0 flex-1">
          <span class="block text-sm font-bold">{{ item.nombre }}</span>
          <span class="block truncate text-xs text-slate-400 group-[.router-link-active]:text-alvid/60">{{ item.descripcion }}</span>
        </span>
        <ChevronRight :size="16" class="opacity-0 transition group-hover:opacity-100" />
      </RouterLink>
    </nav>

    <div class="border-t border-slate-100 p-3">
      <div class="mb-2 flex items-center gap-3 rounded-xl bg-slate-50 p-3">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-alvid text-xs font-black text-white">{{ iniciales }}</div>
        <div class="min-w-0">
          <p class="truncate text-sm font-bold text-slate-900">{{ auth.usuario?.nombre || 'Usuario ALVID' }}</p>
          <p class="truncate text-xs text-slate-500">{{ auth.usuario?.rol || 'Personal' }}</p>
        </div>
      </div>
      <button class="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-bold text-slate-600 transition hover:bg-red-50 hover:text-red-700" type="button" @click="salir">
        <LogOut :size="18" />
        Cerrar sesión
      </button>
    </div>
  </aside>
</template>

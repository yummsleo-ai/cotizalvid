<script setup>
import { computed, onMounted, ref } from 'vue'
import { AlertCircle, Plus, Search, Trash2, X } from '@lucide/vue'

import CotizacionDocumento from '../components/CotizacionDocumento.vue'
import TablaCotizaciones from '../components/TablaCotizaciones.vue'
import { useCotizacionesStore } from '../stores/cotizaciones'

const store = useCotizacionesStore()
const error = ref('')
const busqueda = ref('')
const filtro = ref('todas')
const porEliminar = ref(null)
const documento = ref(null)

onMounted(() => store.cargarCotizaciones())

const cotizacionesFiltradas = computed(() => store.cotizaciones.filter((cotizacion) => {
  const coincideEstado = filtro.value === 'todas' || cotizacion.estado === filtro.value
  const texto = `${cotizacion.nombre_cliente} ${cotizacion.tipo_mueble} ${cotizacion.material?.nombre || ''}`.toLowerCase()
  return coincideEstado && texto.includes(busqueda.value.toLowerCase().trim())
}))

const conteos = computed(() => ({
  todas: store.cotizaciones.length,
  pendiente: store.cotizaciones.filter((item) => item.estado === 'pendiente').length,
  aprobada: store.cotizaciones.filter((item) => item.estado === 'aprobada').length,
  rechazada: store.cotizaciones.filter((item) => item.estado === 'rechazada').length
}))

async function cambiarEstado(id, estado) {
  error.value = ''
  try {
    await store.actualizarCotizacion(id, { estado })
  } catch (err) {
    error.value = err.message
  }
}

async function confirmarEliminar() {
  if (!porEliminar.value) return
  error.value = ''
  try {
    await store.eliminarCotizacion(porEliminar.value.id)
    porEliminar.value = null
  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <div class="grid gap-6">
    <header class="flex flex-wrap items-end justify-between gap-4">
      <div><p class="text-sm font-bold text-alvid">Gestión comercial</p><h1 class="page-title">Cotizaciones</h1><p class="page-description">Encuentra, revisa y da seguimiento a cada propuesta.</p></div>
      <RouterLink class="btn-primary" to="/cotizaciones/nueva"><Plus :size="18" /> Nueva cotización</RouterLink>
    </header>

    <div v-if="error || store.error" class="alert-error"><AlertCircle :size="20" /> {{ error || store.error }}</div>

    <section class="panel min-w-0 overflow-hidden p-4">
      <div class="flex min-w-0 flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <label class="relative block w-full lg:max-w-md">
          <span class="sr-only">Buscar cotizaciones</span>
          <Search :size="18" class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input v-model="busqueda" class="input pl-11" placeholder="Buscar por cliente, mueble o material..." />
          <button v-if="busqueda" class="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100" type="button" aria-label="Limpiar búsqueda" @click="busqueda = ''"><X :size="16" /></button>
        </label>

        <div class="flex max-w-full gap-1 overflow-x-auto rounded-xl bg-slate-100 p-1">
          <button v-for="estado in ['todas', 'pendiente', 'aprobada', 'rechazada']" :key="estado" class="whitespace-nowrap rounded-lg px-3 py-2 text-xs font-bold capitalize transition" :class="filtro === estado ? 'bg-white text-alvid shadow-sm' : 'text-slate-500 hover:text-slate-900'" type="button" @click="filtro = estado">
            {{ estado === 'todas' ? 'Todas' : estado }} <span class="ml-1 text-slate-400">{{ conteos[estado] }}</span>
          </button>
        </div>
      </div>
    </section>

    <div v-if="store.cargando" class="panel overflow-hidden p-5">
      <div v-for="i in 5" :key="i" class="flex items-center gap-4 border-b border-slate-100 py-4 last:border-0"><div class="skeleton h-10 w-10" /><div class="flex-1"><div class="skeleton h-4 w-40" /><div class="skeleton mt-2 h-3 w-24" /></div><div class="skeleton h-8 w-24" /></div>
    </div>
    <TablaCotizaciones v-else :cotizaciones="cotizacionesFiltradas" @estado="cambiarEstado" @eliminar="porEliminar = $event" @documento="documento = $event" />

    <div v-if="porEliminar" class="fixed inset-0 z-[70] grid place-items-center bg-slate-950/40 p-4 backdrop-blur-sm" @click.self="porEliminar = null">
      <section class="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl" role="dialog" aria-modal="true" aria-labelledby="titulo-eliminar">
        <div class="flex h-11 w-11 items-center justify-center rounded-xl bg-red-100 text-red-700"><Trash2 :size="22" /></div>
        <h2 id="titulo-eliminar" class="mt-5 text-xl font-black text-slate-950">¿Eliminar esta cotización?</h2>
        <p class="mt-2 text-sm leading-6 text-slate-600">Se eliminará la cotización de <strong>{{ porEliminar.nombre_cliente }}</strong>. Esta acción no se puede deshacer.</p>
        <div class="mt-6 flex justify-end gap-3"><button class="btn-secondary" type="button" @click="porEliminar = null">Cancelar</button><button class="btn-danger bg-red-600 text-white hover:bg-red-700" type="button" @click="confirmarEliminar">Sí, eliminar</button></div>
      </section>
    </div>

    <CotizacionDocumento v-if="documento" :cotizacion="documento" @cerrar="documento = null" />
  </div>
</template>

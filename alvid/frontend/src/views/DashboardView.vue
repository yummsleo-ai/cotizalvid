<script setup>
import { Bar } from 'vue-chartjs'
import { BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from 'chart.js'
import { computed, onMounted, ref } from 'vue'
import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  CircleDollarSign,
  ClipboardList,
  Clock3,
  PackageSearch,
  Plus,
  TrendingUp,
  XCircle
} from '@lucide/vue'

import { useCotizacionesStore } from '../stores/cotizaciones'

ChartJS.register(BarElement, CategoryScale, LinearScale, Legend, Tooltip)

const store = useCotizacionesStore()
const cargando = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    await store.cargarResumen()
  } catch (err) {
    error.value = err.message
  } finally {
    cargando.value = false
  }
})

const resumen = computed(() => store.resumen || {
  totales_estado: { pendiente: 0, aprobada: 0, rechazada: 0 },
  precio_promedio: 0,
  top_materiales: [],
  ultimas_cotizaciones: [],
  cotizaciones_por_mes: []
})

const totalCotizaciones = computed(() => Object.values(resumen.value.totales_estado).reduce((total, valor) => total + valor, 0))

const chartData = computed(() => ({
  labels: resumen.value.cotizaciones_por_mes.map((item) => item.mes),
  datasets: [{
    label: 'Cotizaciones',
    backgroundColor: '#204A7A',
    hoverBackgroundColor: '#17365D',
    borderRadius: 7,
    borderSkipped: false,
    maxBarThickness: 42,
    data: resumen.value.cotizaciones_por_mes.map((item) => item.total)
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#172033',
      padding: 12,
      cornerRadius: 10,
      displayColors: false
    }
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#64748b', font: { weight: 600 } } },
    y: { beginAtZero: true, grid: { color: '#eef2f6' }, ticks: { precision: 0, color: '#64748b' } }
  }
}

function estadoClase(estado) {
  return {
    pendiente: 'bg-amber-100 text-amber-800',
    aprobada: 'bg-emerald-100 text-emerald-800',
    rechazada: 'bg-red-100 text-red-800'
  }[estado] || 'bg-slate-100 text-slate-700'
}
</script>

<template>
  <div class="grid gap-6">
    <header class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="text-sm font-bold text-alvid">Centro operativo</p>
        <h1 class="page-title">Buen día, revisemos el taller</h1>
        <p class="page-description">Lo más importante del negocio, listo para actuar.</p>
      </div>
      <RouterLink class="btn-primary" to="/cotizaciones/nueva"><Plus :size="18" /> Nueva cotización</RouterLink>
    </header>

    <div v-if="error" class="alert-error"><AlertCircle :size="20" /> {{ error }}</div>

    <template v-if="cargando">
      <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <div v-for="i in 4" :key="i" class="panel p-5"><div class="skeleton h-5 w-28" /><div class="skeleton mt-5 h-9 w-20" /><div class="skeleton mt-4 h-4 w-36" /></div>
      </section>
      <section class="grid gap-6 xl:grid-cols-[minmax(0,1.45fr)_minmax(340px,0.75fr)]">
        <div class="panel p-6"><div class="skeleton h-5 w-44" /><div class="skeleton mt-6 h-72 w-full" /></div>
        <div class="panel p-6"><div class="skeleton h-5 w-36" /><div class="mt-5 grid gap-3"><div v-for="i in 4" :key="i" class="skeleton h-16 w-full" /></div></div>
      </section>
    </template>

    <template v-else>
      <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <RouterLink to="/cotizaciones" class="panel group p-5 transition-all hover:-translate-y-0.5 hover:border-amber-300 hover:shadow-lg">
          <div class="flex items-start justify-between">
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-100 text-amber-700"><Clock3 :size="21" /></span>
            <ArrowRight :size="18" class="text-slate-300 transition group-hover:translate-x-1 group-hover:text-amber-600" />
          </div>
          <p class="mt-5 text-3xl font-black text-slate-950">{{ resumen.totales_estado.pendiente }}</p>
          <p class="mt-1 text-sm font-bold text-slate-700">Cotizaciones pendientes</p>
          <p class="mt-2 text-xs text-slate-500">Requieren seguimiento</p>
        </RouterLink>

        <div class="panel p-5">
          <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700"><CheckCircle2 :size="21" /></span>
          <p class="mt-5 text-3xl font-black text-slate-950">{{ resumen.totales_estado.aprobada }}</p>
          <p class="mt-1 text-sm font-bold text-slate-700">Trabajos aprobados</p>
          <p class="mt-2 text-xs text-emerald-700">Listos para producción</p>
        </div>

        <div class="panel p-5">
          <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-100 text-blue-700"><CircleDollarSign :size="21" /></span>
          <p class="mt-5 text-2xl font-black text-slate-950">{{ resumen.precio_promedio.toFixed(2) }} <span class="text-base">Bs</span></p>
          <p class="mt-1 text-sm font-bold text-slate-700">Valor promedio</p>
          <p class="mt-2 text-xs text-slate-500">Por cotización registrada</p>
        </div>

        <div class="panel p-5">
          <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-700"><TrendingUp :size="21" /></span>
          <p class="mt-5 text-3xl font-black text-slate-950">{{ totalCotizaciones }}</p>
          <p class="mt-1 text-sm font-bold text-slate-700">Cotizaciones totales</p>
          <p class="mt-2 flex items-center gap-1 text-xs text-slate-500"><XCircle :size="13" /> {{ resumen.totales_estado.rechazada }} no concretadas</p>
        </div>
      </section>

      <section class="grid gap-6 xl:grid-cols-[minmax(0,1.45fr)_minmax(340px,0.75fr)]">
        <div class="panel min-w-0 p-5 sm:p-6">
          <div class="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 class="section-title">Actividad de cotizaciones</h2>
              <p class="mt-1 text-sm text-slate-500">Cantidad registrada por mes</p>
            </div>
            <span class="badge bg-blue-50 text-alvid">Tendencia</span>
          </div>
          <div v-if="resumen.cotizaciones_por_mes.length" class="mt-6 h-72">
            <Bar :data="chartData" :options="chartOptions" />
          </div>
          <div v-else class="mt-6 grid h-72 place-items-center rounded-xl border border-dashed border-slate-300 bg-slate-50 text-center">
            <div><TrendingUp :size="30" class="mx-auto text-slate-300" /><p class="mt-3 text-sm font-bold text-slate-700">Aún no hay tendencia</p><p class="mt-1 text-xs text-slate-500">Aparecerá al registrar cotizaciones.</p></div>
          </div>
        </div>

        <div class="panel p-5 sm:p-6">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="section-title">Actividad reciente</h2>
              <p class="mt-1 text-sm text-slate-500">Últimos movimientos</p>
            </div>
            <RouterLink to="/cotizaciones" class="text-xs font-bold text-alvid hover:underline">Ver todas</RouterLink>
          </div>
          <ul v-if="resumen.ultimas_cotizaciones.length" class="mt-5 divide-y divide-slate-100">
            <li v-for="cotizacion in resumen.ultimas_cotizaciones" :key="cotizacion.id" class="py-4 first:pt-0">
              <div class="flex items-start justify-between gap-3">
                <div class="min-w-0">
                  <p class="truncate text-sm font-bold text-slate-900">{{ cotizacion.nombre_cliente }}</p>
                  <p class="mt-0.5 truncate text-xs text-slate-500">{{ cotizacion.tipo_mueble }} · {{ cotizacion.material || 'Sin material' }}</p>
                </div>
                <span class="badge shrink-0" :class="estadoClase(cotizacion.estado)">{{ cotizacion.estado }}</span>
              </div>
              <p class="mt-2 text-sm font-black text-alvid">{{ cotizacion.precio_final_bs.toFixed(2) }} Bs</p>
            </li>
          </ul>
          <div v-else class="mt-8 text-center">
            <ClipboardList :size="30" class="mx-auto text-slate-300" />
            <p class="mt-3 text-sm font-bold text-slate-700">Sin actividad reciente</p>
          </div>
        </div>
      </section>

      <section class="panel p-5 sm:p-6">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 class="section-title">Materiales más utilizados</h2>
            <p class="mt-1 text-sm text-slate-500">Referencia rápida para planificar compras</p>
          </div>
          <RouterLink class="btn-secondary" to="/materiales"><PackageSearch :size="18" /> Revisar inventario</RouterLink>
        </div>
        <div v-if="resumen.top_materiales.length" class="mt-5 grid gap-3 md:grid-cols-3">
          <div v-for="(material, index) in resumen.top_materiales" :key="material.nombre" class="flex items-center gap-4 rounded-xl border border-slate-200 bg-slate-50/60 p-4">
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-sm font-black text-alvid shadow-sm">{{ index + 1 }}</span>
            <div class="min-w-0"><p class="truncate text-sm font-bold text-slate-900">{{ material.nombre }}</p><p class="mt-0.5 text-xs text-slate-500">{{ material.total }} cotizaciones</p></div>
          </div>
        </div>
        <p v-else class="mt-5 rounded-xl bg-slate-50 p-5 text-center text-sm text-slate-500">Aún no hay uso de materiales registrado.</p>
      </section>
    </template>
  </div>
</template>

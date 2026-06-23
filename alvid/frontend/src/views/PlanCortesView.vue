<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { AlertCircle, Layers3, Plus, Ruler, Sparkles, Trash2 } from '@lucide/vue'

import VisualizadorCortes from '../components/VisualizadorCortes.vue'
import { useCotizacionesStore } from '../stores/cotizaciones'
import { useMaterialesStore } from '../stores/materiales'

const cotizacionesStore = useCotizacionesStore()
const materialesStore = useMaterialesStore()
const error = ref('')
const plan = ref(null)
const generando = ref(false)
const form = reactive({
  cotizacion_id: '',
  tablero_id: '',
  piezas: [
    { etiqueta: 'Lateral', largo: 1800, ancho: 500, cantidad: 2 },
    { etiqueta: 'Base', largo: 1200, ancho: 500, cantidad: 2 },
    { etiqueta: 'Puerta', largo: 1750, ancho: 580, cantidad: 2 }
  ]
})

const cotizacionesDisponibles = computed(() => cotizacionesStore.cotizaciones)
const materialesDisponibles = computed(() => materialesStore.materiales)
const totalPiezas = computed(() => form.piezas.reduce((total, pieza) => total + Number(pieza.cantidad || 0), 0))
const cotizacionSeleccionada = computed(() => cotizacionesDisponibles.value.find((item) => item.id === Number(form.cotizacion_id)))
const materialSeleccionado = computed(() => materialesDisponibles.value.find((item) => item.id === Number(form.tablero_id)))

onMounted(async () => {
  await Promise.all([cotizacionesStore.cargarCotizaciones(), materialesStore.cargarMateriales()])
  form.cotizacion_id = cotizacionesDisponibles.value[0]?.id || ''
  form.tablero_id = materialesDisponibles.value[0]?.id || ''
})

function agregarPieza() {
  form.piezas.push({ etiqueta: `Pieza ${form.piezas.length + 1}`, largo: 600, ancho: 300, cantidad: 1 })
}

function quitarPieza(indice) {
  if (form.piezas.length > 1) form.piezas.splice(indice, 1)
}

async function generar() {
  error.value = ''
  plan.value = null
  generando.value = true
  try {
    plan.value = await cotizacionesStore.generarPlanCorte({
      cotizacion_id: Number(form.cotizacion_id),
      tablero_id: Number(form.tablero_id),
      piezas: form.piezas.map((pieza) => ({ etiqueta: pieza.etiqueta, largo: Number(pieza.largo), ancho: Number(pieza.ancho), cantidad: Number(pieza.cantidad) }))
    })
  } catch (err) {
    error.value = err.message
  } finally {
    generando.value = false
  }
}
</script>

<template>
  <div class="grid gap-6">
    <header><p class="text-sm font-bold text-alvid">Optimización de material</p><h1 class="page-title">Plan de cortes</h1><p class="page-description">Organiza las piezas y aprovecha mejor cada tablero.</p></header>

    <form class="grid gap-6 xl:grid-cols-[340px_minmax(0,1fr)]" @submit.prevent="generar">
      <aside class="panel h-fit p-5 xl:sticky xl:top-8">
        <div class="flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-alvid-50 text-alvid"><Layers3 :size="20" /></span><div><h2 class="section-title">Configuración</h2><p class="text-xs text-slate-500">Trabajo y tablero base</p></div></div>
        <div class="mt-6 grid gap-5">
          <label class="grid gap-2"><span class="label">Cotización</span><select v-model="form.cotizacion_id" class="input" required><option v-for="cotizacion in cotizacionesDisponibles" :key="cotizacion.id" :value="cotizacion.id">#{{ cotizacion.id }} · {{ cotizacion.nombre_cliente }} · {{ cotizacion.tipo_mueble }}</option></select></label>
          <label class="grid gap-2"><span class="label">Tablero a utilizar</span><select v-model="form.tablero_id" class="input" required><option v-for="material in materialesDisponibles" :key="material.id" :value="material.id">{{ material.nombre }} · {{ material.largo_mm }} × {{ material.ancho_mm }} mm</option></select></label>
        </div>
        <div class="mt-6 rounded-xl bg-slate-50 p-4">
          <dl class="grid gap-3 text-sm"><div class="flex justify-between gap-3"><dt class="text-slate-500">Cliente</dt><dd class="truncate font-bold">{{ cotizacionSeleccionada?.nombre_cliente || 'Sin seleccionar' }}</dd></div><div class="flex justify-between gap-3"><dt class="text-slate-500">Tablero</dt><dd class="truncate font-bold">{{ materialSeleccionado?.nombre || 'Sin seleccionar' }}</dd></div><div class="flex justify-between gap-3"><dt class="text-slate-500">Total piezas</dt><dd class="font-black text-alvid">{{ totalPiezas }}</dd></div></dl>
        </div>
        <button class="btn-primary mt-5 w-full py-3" type="submit" :disabled="generando || !form.cotizacion_id || !form.tablero_id"><span v-if="generando" class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" /><Sparkles v-else :size="18" />{{ generando ? 'Optimizando...' : 'Generar plan de cortes' }}</button>
        <div v-if="error" class="alert-error mt-4"><AlertCircle :size="20" class="shrink-0" />{{ error }}</div>
      </aside>

      <section class="panel p-5 sm:p-6">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div><h2 class="section-title">Lista de piezas</h2><p class="mt-1 text-sm text-slate-500">Agrega cada parte que necesitas cortar.</p></div>
          <button class="btn-secondary" type="button" @click="agregarPieza"><Plus :size="17" /> Agregar pieza</button>
        </div>

        <div class="mt-6 grid gap-4">
          <article v-for="(pieza, indice) in form.piezas" :key="indice" class="rounded-2xl border border-slate-200 bg-slate-50/50 p-4 transition hover:border-slate-300">
            <div class="flex items-start gap-3">
              <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-sm font-black text-alvid shadow-sm">{{ indice + 1 }}</span>
              <div class="grid min-w-0 flex-1 gap-3 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_0.7fr]">
                <label class="grid gap-1"><span class="helper">Nombre de pieza</span><input v-model="pieza.etiqueta" class="input" placeholder="Ej. Lateral izquierdo" required /></label>
                <label class="grid gap-1"><span class="helper">Largo (mm)</span><input v-model.number="pieza.largo" class="input" min="1" type="number" required /></label>
                <label class="grid gap-1"><span class="helper">Ancho (mm)</span><input v-model.number="pieza.ancho" class="input" min="1" type="number" required /></label>
                <label class="grid gap-1"><span class="helper">Cantidad</span><input v-model.number="pieza.cantidad" class="input" min="1" type="number" required /></label>
              </div>
              <button class="icon-button mt-6 text-red-600 hover:bg-red-50" type="button" :disabled="form.piezas.length === 1" :aria-label="`Quitar ${pieza.etiqueta}`" @click="quitarPieza(indice)"><Trash2 :size="17" /></button>
            </div>
            <div class="mt-3 flex items-center gap-2 pl-0 text-xs text-slate-500 sm:pl-14"><Ruler :size="14" /> Área total: {{ ((pieza.largo * pieza.ancho * pieza.cantidad) / 1000000).toFixed(2) }} m²</div>
          </article>
        </div>
      </section>
    </form>

    <VisualizadorCortes v-if="plan" :plan="plan" :proyecto="cotizacionSeleccionada" :material="materialSeleccionado" />
  </div>
</template>

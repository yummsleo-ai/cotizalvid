<script setup>
import { computed, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight, CheckCircle2, Layers3, Printer, Scissors, TriangleAlert } from '@lucide/vue'

const props = defineProps({
  plan: { type: Object, default: null },
  proyecto: { type: Object, default: null },
  material: { type: Object, default: null }
})

const indice = ref(0)
const tableros = computed(() => props.plan?.tableros || props.plan?.detalle_json?.tableros || [])
const tableroActual = computed(() => tableros.value[indice.value] || null)
const escalaTexto = computed(() => (tableroActual.value ? Math.max(tableroActual.value.largo, tableroActual.value.ancho) / 40 : 24))
const eficiencia = computed(() => props.plan?.eficiencia_pct || props.plan?.eficiencia_porcentaje || 0)
const desperdicio = computed(() => props.plan?.desperdicio_pct || props.plan?.desperdicio_porcentaje || 0)

watch(tableros, () => { indice.value = 0 })

function color(indicePieza) {
  const colores = ['#204A7A', '#A86416', '#15803D', '#6D5BD0', '#C2415D', '#0F766E', '#475569', '#C45A20']
  return colores[indicePieza % colores.length]
}

function imprimir() {
  window.print()
}
</script>

<template>
  <section v-if="tableroActual" class="panel overflow-hidden print:border-0 print:shadow-none">
    <header class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 bg-slate-50/70 p-5 sm:p-6">
      <div class="flex items-center gap-3">
        <img src="/logo-alvid.png" alt="ALVID" class="hidden h-16 w-16 object-contain print:block" />
        <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-alvid text-white print:hidden"><Scissors :size="22" /></span>
        <div><p class="text-xs font-bold uppercase text-alvid">Resultado optimizado</p><h2 class="text-xl font-black text-slate-950">Plan de cortes</h2><p class="mt-0.5 text-xs text-slate-500">{{ proyecto?.nombre_cliente }} · {{ material?.nombre }}</p></div>
      </div>
      <button class="btn-secondary no-print" type="button" @click="imprimir"><Printer :size="18" /> Imprimir / PDF</button>
    </header>

    <div class="grid gap-5 p-5 sm:p-6 lg:grid-cols-[minmax(0,1fr)_280px]">
      <div class="min-w-0">
        <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div><p class="text-sm font-black text-slate-900">Tablero {{ indice + 1 }} de {{ tableros.length }}</p><p class="text-xs text-slate-500">{{ tableroActual.largo }} × {{ tableroActual.ancho }} mm · {{ tableroActual.piezas.length }} piezas</p></div>
          <div class="no-print flex gap-2">
            <button class="icon-button" type="button" :disabled="indice === 0" aria-label="Tablero anterior" @click="indice--"><ArrowLeft :size="18" /></button>
            <button class="icon-button" type="button" :disabled="indice >= tableros.length - 1" aria-label="Tablero siguiente" @click="indice++"><ArrowRight :size="18" /></button>
          </div>
        </div>

        <div class="overflow-x-auto rounded-2xl border border-slate-200 bg-[#e9edf1] p-3 sm:p-5">
          <svg class="h-auto w-full min-w-[620px] drop-shadow-md" :viewBox="`0 0 ${tableroActual.largo} ${tableroActual.ancho}`" role="img" :aria-label="`Distribución de piezas del tablero ${indice + 1}`">
            <rect x="0" y="0" :width="tableroActual.largo" :height="tableroActual.ancho" rx="12" fill="#FFFFFF" stroke="#334155" stroke-width="8" />
            <g v-for="(pieza, i) in tableroActual.piezas" :key="`${pieza.etiqueta}-${i}`">
              <rect :x="pieza.x" :y="pieza.y" :width="pieza.largo" :height="pieza.ancho" :fill="color(i)" fill-opacity="0.9" stroke="#FFFFFF" stroke-width="7" />
              <text :x="pieza.x + 16" :y="pieza.y + escalaTexto" fill="#FFFFFF" :font-size="escalaTexto" font-weight="800">{{ pieza.etiqueta }}</text>
              <text :x="pieza.x + 16" :y="pieza.y + escalaTexto * 2.05" fill="#FFFFFF" :font-size="escalaTexto * 0.7">{{ Math.round(pieza.largo) }} × {{ Math.round(pieza.ancho) }} mm</text>
            </g>
          </svg>
        </div>
      </div>

      <aside class="grid content-start gap-4">
        <div class="rounded-2xl border border-emerald-200 bg-emerald-50 p-5">
          <div class="flex items-center justify-between"><span class="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-emerald-700 shadow-sm"><CheckCircle2 :size="20" /></span><span class="text-xs font-bold text-emerald-700">Buen aprovechamiento</span></div>
          <p class="mt-4 text-3xl font-black text-emerald-800">{{ eficiencia }}%</p><p class="mt-1 text-sm font-bold text-emerald-800">Eficiencia total</p>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div class="rounded-2xl border border-slate-200 bg-white p-4"><Layers3 :size="19" class="text-alvid" /><p class="mt-3 text-2xl font-black">{{ props.plan.total_tableros || props.plan.tableros_necesarios }}</p><p class="text-xs text-slate-500">Tableros</p></div>
          <div class="rounded-2xl border border-amber-200 bg-amber-50 p-4"><TriangleAlert :size="19" class="text-amber-700" /><p class="mt-3 text-2xl font-black text-amber-800">{{ desperdicio }}%</p><p class="text-xs text-amber-700">Desperdicio</p></div>
        </div>
        <div class="rounded-2xl border border-slate-200 p-4">
          <p class="text-xs font-black uppercase text-slate-500">Piezas en este tablero</p>
          <ul class="mt-3 grid gap-2">
            <li v-for="(pieza, i) in tableroActual.piezas" :key="`lista-${i}`" class="flex items-center gap-2 text-xs"><span class="h-3 w-3 rounded-sm" :style="{ backgroundColor: color(i) }" /><span class="min-w-0 flex-1 truncate font-bold text-slate-700">{{ pieza.etiqueta }}</span><span class="text-slate-400">{{ Math.round(pieza.largo) }}×{{ Math.round(pieza.ancho) }}</span></li>
          </ul>
        </div>
      </aside>
    </div>
  </section>
</template>

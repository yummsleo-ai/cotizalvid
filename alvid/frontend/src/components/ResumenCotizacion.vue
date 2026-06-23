<script setup>
import { CheckCircle2, Sparkles } from '@lucide/vue'

defineProps({
  prediccion: { type: Object, default: null },
  precioFinal: { type: [Number, String], default: '' },
  compacto: { type: Boolean, default: false }
})
</script>

<template>
  <section class="overflow-hidden rounded-2xl border border-alvid/15 bg-alvid text-white shadow-lg">
    <div class="p-5 sm:p-6">
      <div class="flex items-center gap-2 text-blue-100"><Sparkles :size="18" /><p class="text-xs font-black uppercase">Estimación ALVID</p></div>
      <p class="mt-4 text-sm text-blue-100">Precio final de la cotización</p>
      <p class="mt-1 text-3xl font-black sm:text-4xl">{{ Number(precioFinal || prediccion?.precio_estimado_bs || 0).toFixed(2) }} <span class="text-lg">Bs</span></p>

      <div v-if="prediccion" class="mt-5 grid grid-cols-2 gap-3 border-t border-white/15 pt-5">
        <div><p class="text-xs text-blue-200">Sugerencia del sistema</p><p class="mt-1 text-sm font-black">{{ prediccion.precio_estimado_bs.toFixed(2) }} Bs</p></div>
        <div><p class="text-xs text-blue-200">Nivel de confianza</p><p class="mt-1 flex items-center gap-1 text-sm font-black"><CheckCircle2 :size="15" class="text-emerald-300" />{{ Math.round(prediccion.confianza * 100) }}%</p></div>
      </div>
      <p v-else class="mt-4 text-xs leading-5 text-blue-200">Completa material y medidas para obtener una estimación automática.</p>
    </div>
  </section>
</template>

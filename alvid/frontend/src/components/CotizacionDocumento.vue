<script setup>
import { Printer, X } from '@lucide/vue'

defineProps({
  cotizacion: {
    type: Object,
    required: true
  }
})

defineEmits(['cerrar'])

function imprimir() {
  window.print()
}
</script>

<template>
  <div class="fixed inset-0 z-[70] overflow-y-auto bg-slate-950/60 p-3 backdrop-blur-sm print:static print:bg-white print:p-0">
    <div class="no-print sticky top-3 z-10 mx-auto mb-3 flex max-w-4xl justify-end gap-2">
      <button class="btn-secondary" type="button" @click="$emit('cerrar')"><X :size="18" /> Cerrar</button>
      <button class="btn-primary" type="button" @click="imprimir"><Printer :size="18" /> Guardar como PDF</button>
    </div>

    <article class="mx-auto min-h-[1050px] max-w-4xl bg-white p-8 text-slate-900 shadow-2xl print:min-h-0 print:max-w-none print:p-0 print:shadow-none sm:p-12">
      <header class="flex items-start justify-between gap-8 border-b-2 border-alvid pb-7">
        <div class="flex items-center gap-4">
          <img src="/logo-alvid.png" alt="ALVID" class="h-24 w-24 object-contain" />
          <div>
            <h1 class="text-3xl font-black text-alvid">ALVID</h1>
            <p class="text-sm font-semibold text-slate-500">Soluciones profesionales en carpintería</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-xs font-bold uppercase text-slate-500">Cotización</p>
          <p class="mt-1 text-2xl font-black text-slate-900">#{{ String(cotizacion.id).padStart(4, '0') }}</p>
          <p class="mt-1 text-xs text-slate-500">{{ new Date(cotizacion.created_at).toLocaleDateString('es-BO') }}</p>
        </div>
      </header>

      <section class="mt-8 grid gap-6 sm:grid-cols-2">
        <div>
          <p class="text-xs font-bold uppercase text-slate-500">Preparado para</p>
          <p class="mt-2 text-lg font-black">{{ cotizacion.nombre_cliente }}</p>
          <p class="mt-1 text-sm text-slate-600">{{ cotizacion.tipo_mueble }}</p>
        </div>
        <div class="sm:text-right">
          <p class="text-xs font-bold uppercase text-slate-500">Estado</p>
          <p class="mt-2 text-sm font-black capitalize">{{ cotizacion.estado }}</p>
          <p class="mt-1 text-sm text-slate-600">Validez sujeta a disponibilidad de material</p>
        </div>
      </section>

      <section class="mt-8 rounded-xl border border-slate-200">
        <div class="border-b border-slate-200 bg-slate-50 px-5 py-3">
          <h2 class="text-sm font-black uppercase text-slate-700">Detalle del proyecto</h2>
        </div>
        <div class="grid gap-5 p-5 sm:grid-cols-2">
          <div><p class="text-xs font-bold text-slate-500">Material</p><p class="mt-1 text-sm font-semibold">{{ cotizacion.material?.nombre || 'Sin material especificado' }}</p></div>
          <div><p class="text-xs font-bold text-slate-500">Medidas generales</p><p class="mt-1 text-sm font-semibold">{{ cotizacion.largo_mm }} × {{ cotizacion.ancho_mm }} × {{ cotizacion.alto_mm }} mm</p></div>
          <div><p class="text-xs font-bold text-slate-500">Cantidad de piezas</p><p class="mt-1 text-sm font-semibold">{{ cotizacion.cantidad_piezas }}</p></div>
          <div><p class="text-xs font-bold text-slate-500">Tipo de trabajo</p><p class="mt-1 text-sm font-semibold">{{ cotizacion.tipo_mueble }}</p></div>
          <div class="sm:col-span-2"><p class="text-xs font-bold text-slate-500">Descripción</p><p class="mt-1 whitespace-pre-line text-sm leading-6 text-slate-700">{{ cotizacion.descripcion }}</p></div>
        </div>
      </section>

      <section class="mt-8">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b-2 border-slate-900 text-left text-xs uppercase text-slate-500">
              <th class="py-3">Concepto</th>
              <th class="py-3 text-right">Importe</th>
            </tr>
          </thead>
          <tbody>
            <tr class="border-b border-slate-200">
              <td class="py-4"><p class="font-bold">Fabricación de {{ cotizacion.tipo_mueble }}</p><p class="mt-1 text-xs text-slate-500">Incluye material, fabricación y armado según especificación.</p></td>
              <td class="py-4 text-right font-bold">{{ cotizacion.precio_final_bs.toFixed(2) }} Bs</td>
            </tr>
          </tbody>
        </table>
        <div class="ml-auto mt-5 max-w-xs">
          <div class="flex items-center justify-between border-t-2 border-alvid pt-4">
            <span class="text-base font-black">TOTAL</span>
            <span class="text-2xl font-black text-alvid">{{ cotizacion.precio_final_bs.toFixed(2) }} Bs</span>
          </div>
        </div>
      </section>

      <section class="mt-10 rounded-xl bg-slate-50 p-5">
        <h2 class="text-xs font-black uppercase text-slate-600">Observaciones</h2>
        <p class="mt-2 text-xs leading-5 text-slate-600">El precio final puede variar ante cambios de medidas, material o alcance solicitados después de la aprobación. Los tiempos de entrega se coordinan al confirmar el trabajo.</p>
      </section>

      <footer class="mt-20 grid gap-10 sm:grid-cols-2">
        <div class="border-t border-slate-400 pt-3 text-center text-xs font-semibold text-slate-600">Firma ALVID</div>
        <div class="border-t border-slate-400 pt-3 text-center text-xs font-semibold text-slate-600">Firma del cliente</div>
      </footer>
    </article>
  </div>
</template>

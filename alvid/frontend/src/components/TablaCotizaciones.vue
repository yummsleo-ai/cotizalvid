<script setup>
import { FileText, MoreHorizontal, Trash2 } from '@lucide/vue'

defineProps({
  cotizaciones: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['estado', 'eliminar', 'documento'])

function badgeClase(estado) {
  return {
    pendiente: 'bg-amber-100 text-amber-800',
    aprobada: 'bg-emerald-100 text-emerald-800',
    rechazada: 'bg-red-100 text-red-800'
  }[estado] || 'bg-slate-100 text-slate-700'
}

function iniciales(nombre) {
  return nombre.split(' ').slice(0, 2).map((parte) => parte[0]).join('').toUpperCase()
}
</script>

<template>
  <div v-if="cotizaciones.length" class="panel overflow-hidden">
    <div class="hidden overflow-x-auto md:block">
      <table class="min-w-full text-sm">
        <thead class="border-b border-slate-200 bg-slate-50/80 text-left text-xs font-bold uppercase text-slate-500">
          <tr>
            <th class="px-5 py-3.5">Cliente / proyecto</th>
            <th class="px-5 py-3.5">Material</th>
            <th class="px-5 py-3.5">Importe</th>
            <th class="px-5 py-3.5">Estado</th>
            <th class="px-5 py-3.5 text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="cotizacion in cotizaciones" :key="cotizacion.id" class="transition hover:bg-slate-50/70">
            <td class="px-5 py-4">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-alvid-50 text-xs font-black text-alvid">{{ iniciales(cotizacion.nombre_cliente) }}</div>
                <div><p class="font-bold text-slate-900">{{ cotizacion.nombre_cliente }}</p><p class="mt-0.5 text-xs text-slate-500">#{{ cotizacion.id }} · {{ cotizacion.tipo_mueble }}</p></div>
              </div>
            </td>
            <td class="max-w-[220px] px-5 py-4"><p class="truncate font-semibold text-slate-700">{{ cotizacion.material?.nombre || 'Sin material' }}</p><p class="mt-0.5 text-xs text-slate-500">{{ cotizacion.cantidad_piezas }} piezas</p></td>
            <td class="whitespace-nowrap px-5 py-4 font-black text-alvid">{{ cotizacion.precio_final_bs.toFixed(2) }} Bs</td>
            <td class="px-5 py-4"><span class="badge" :class="badgeClase(cotizacion.estado)"><span class="h-1.5 w-1.5 rounded-full bg-current" />{{ cotizacion.estado }}</span></td>
            <td class="px-5 py-4">
              <div class="flex items-center justify-end gap-2">
                <label class="sr-only" :for="`estado-${cotizacion.id}`">Cambiar estado</label>
                <select :id="`estado-${cotizacion.id}`" class="input min-h-9 w-32 py-1.5 text-xs font-bold capitalize" :value="cotizacion.estado" @change="emit('estado', cotizacion.id, $event.target.value)">
                  <option value="pendiente">Pendiente</option><option value="aprobada">Aprobada</option><option value="rechazada">Rechazada</option>
                </select>
                <button class="icon-button h-9 w-9" type="button" title="Ver documento" aria-label="Ver documento" @click="emit('documento', cotizacion)"><FileText :size="17" /></button>
                <button class="icon-button h-9 w-9 text-red-600 hover:bg-red-50 hover:text-red-700" type="button" title="Eliminar cotización" aria-label="Eliminar cotización" @click="emit('eliminar', cotizacion)"><Trash2 :size="17" /></button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="divide-y divide-slate-100 md:hidden">
      <article v-for="cotizacion in cotizaciones" :key="cotizacion.id" class="p-4">
        <div class="flex items-start justify-between gap-3">
          <div class="flex min-w-0 items-center gap-3">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-alvid-50 text-xs font-black text-alvid">{{ iniciales(cotizacion.nombre_cliente) }}</div>
            <div class="min-w-0"><p class="truncate font-bold text-slate-900">{{ cotizacion.nombre_cliente }}</p><p class="truncate text-xs text-slate-500">#{{ cotizacion.id }} · {{ cotizacion.tipo_mueble }}</p></div>
          </div>
          <span class="badge shrink-0" :class="badgeClase(cotizacion.estado)">{{ cotizacion.estado }}</span>
        </div>
        <div class="mt-4 grid grid-cols-2 gap-3 rounded-xl bg-slate-50 p-3">
          <div><p class="text-xs text-slate-500">Material</p><p class="mt-1 truncate text-sm font-bold">{{ cotizacion.material?.nombre || 'Sin material' }}</p></div>
          <div class="text-right"><p class="text-xs text-slate-500">Importe</p><p class="mt-1 text-sm font-black text-alvid">{{ cotizacion.precio_final_bs.toFixed(2) }} Bs</p></div>
        </div>
        <div class="mt-3 flex gap-2">
          <select class="input min-h-10 flex-1 py-2 text-xs font-bold capitalize" :value="cotizacion.estado" @change="emit('estado', cotizacion.id, $event.target.value)">
            <option value="pendiente">Pendiente</option><option value="aprobada">Aprobada</option><option value="rechazada">Rechazada</option>
          </select>
          <button class="icon-button" type="button" aria-label="Ver documento" @click="emit('documento', cotizacion)"><FileText :size="18" /></button>
          <button class="icon-button text-red-600" type="button" aria-label="Eliminar" @click="emit('eliminar', cotizacion)"><Trash2 :size="18" /></button>
        </div>
      </article>
    </div>
  </div>

  <div v-else class="panel grid min-h-72 place-items-center p-8 text-center">
    <div><MoreHorizontal :size="36" class="mx-auto text-slate-300" /><h3 class="mt-4 text-base font-black text-slate-800">No encontramos cotizaciones</h3><p class="mt-1 text-sm text-slate-500">Prueba otro filtro o crea una nueva cotización.</p></div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import {
  AlertCircle,
  ArrowLeft,
  ArrowRight,
  Check,
  ClipboardCheck,
  Layers3,
  Package,
  Ruler,
  Sparkles,
  UserRound
} from '@lucide/vue'

import { useCotizacionesStore } from '../stores/cotizaciones'
import { useMaterialesStore } from '../stores/materiales'
import ResumenCotizacion from './ResumenCotizacion.vue'

const emit = defineEmits(['guardada'])
const materialesStore = useMaterialesStore()
const cotizacionesStore = useCotizacionesStore()
const error = ref('')
const guardando = ref(false)
const prediciendo = ref(false)
const prediccion = ref(null)
const precioFinalEditado = ref(false)
const paso = ref(1)

const pasos = [
  { numero: 1, nombre: 'Cliente', icono: UserRound },
  { numero: 2, nombre: 'Mueble', icono: Layers3 },
  { numero: 3, nombre: 'Material', icono: Package },
  { numero: 4, nombre: 'Medidas', icono: Ruler },
  { numero: 5, nombre: 'Resultado', icono: ClipboardCheck }
]

const tiposMueble = ['Ropero', 'Cocina', 'Escritorio', 'Mesa', 'Estante', 'Puerta', 'Otro']

const form = reactive({
  nombre_cliente: '',
  descripcion: '',
  tipo_mueble: 'Ropero',
  cantidad_piezas: 6,
  material_id: '',
  largo_mm: 1200,
  ancho_mm: 500,
  alto_mm: 1800,
  precio_final_bs: '',
  estado: 'pendiente'
})

const materialSeleccionado = computed(() => materialesStore.materiales.find((material) => material.id === Number(form.material_id)))
const puedePredecir = computed(() => form.material_id && form.largo_mm > 0 && form.ancho_mm > 0 && form.alto_mm > 0 && form.cantidad_piezas > 0)
const progreso = computed(() => `${((paso.value - 1) / 4) * 100}%`)

onMounted(async () => {
  await materialesStore.cargarMateriales()
  if (!form.material_id && materialesStore.materiales.length) form.material_id = materialesStore.materiales[0].id
})

watch(
  () => [form.material_id, form.largo_mm, form.ancho_mm, form.alto_mm, form.cantidad_piezas],
  () => {
    prediccion.value = null
    if (!precioFinalEditado.value) form.precio_final_bs = ''
  }
)

function siguiente() {
  error.value = ''
  if (paso.value === 1 && !form.nombre_cliente.trim()) {
    error.value = 'Escribe el nombre del cliente para continuar.'
    return
  }
  if (paso.value === 2 && (!form.tipo_mueble.trim() || !form.descripcion.trim())) {
    error.value = 'Selecciona el mueble y agrega una breve descripción.'
    return
  }
  if (paso.value === 3 && !form.material_id) {
    error.value = 'Selecciona el material principal del trabajo.'
    return
  }
  if (paso.value === 4 && !puedePredecir.value) {
    error.value = 'Revisa que todas las medidas y la cantidad sean mayores a cero.'
    return
  }
  if (paso.value < 5) paso.value++
  if (paso.value === 5 && !prediccion.value) predecir()
}

function anterior() {
  error.value = ''
  if (paso.value > 1) paso.value--
}

async function predecir() {
  if (!puedePredecir.value) return
  error.value = ''
  prediciendo.value = true
  try {
    prediccion.value = await cotizacionesStore.predecir({
      material_id: Number(form.material_id),
      largo_mm: Number(form.largo_mm),
      ancho_mm: Number(form.ancho_mm),
      alto_mm: Number(form.alto_mm),
      cantidad_piezas: Number(form.cantidad_piezas)
    })
    if (!precioFinalEditado.value || !form.precio_final_bs) {
      form.precio_final_bs = prediccion.value.precio_estimado_bs
      precioFinalEditado.value = false
    }
  } catch (err) {
    error.value = err.message
  } finally {
    prediciendo.value = false
  }
}

async function guardar() {
  error.value = ''
  guardando.value = true
  try {
    if (!prediccion.value) await predecir()
    const payload = {
      ...form,
      material_id: Number(form.material_id),
      cantidad_piezas: Number(form.cantidad_piezas),
      largo_mm: Number(form.largo_mm),
      ancho_mm: Number(form.ancho_mm),
      alto_mm: Number(form.alto_mm),
      precio_final_bs: Number(form.precio_final_bs || prediccion.value?.precio_estimado_bs || 0)
    }
    const cotizacion = await cotizacionesStore.crearCotizacion(payload)
    emit('guardada', cotizacion)
  } catch (err) {
    error.value = err.message
  } finally {
    guardando.value = false
  }
}
</script>

<template>
  <div class="grid gap-6 xl:grid-cols-[minmax(0,1fr)_340px]">
    <section class="panel overflow-hidden">
      <div class="border-b border-slate-200 bg-slate-50/70 px-4 py-5 sm:px-6">
        <div class="relative">
          <div class="absolute left-5 right-5 top-5 h-0.5 bg-slate-200 sm:left-8 sm:right-8">
            <div class="h-full bg-alvid transition-all duration-500" :style="{ width: progreso }" />
          </div>
          <ol class="relative flex justify-between">
            <li v-for="item in pasos" :key="item.numero" class="flex flex-col items-center gap-2">
              <button class="flex h-10 w-10 items-center justify-center rounded-full border-2 text-sm font-black transition-all" :class="paso >= item.numero ? 'border-alvid bg-alvid text-white shadow-md' : 'border-slate-200 bg-white text-slate-400'" type="button" :aria-label="`Ir a ${item.nombre}`" :disabled="item.numero > paso" @click="paso = item.numero">
                <Check v-if="paso > item.numero" :size="17" />
                <component :is="item.icono" v-else :size="17" />
              </button>
              <span class="hidden text-xs font-bold sm:block" :class="paso >= item.numero ? 'text-alvid' : 'text-slate-400'">{{ item.nombre }}</span>
            </li>
          </ol>
        </div>
      </div>

      <form class="p-5 sm:p-7" @submit.prevent="guardar">
        <div class="min-h-[390px]">
          <section v-if="paso === 1">
            <p class="text-sm font-bold text-alvid">Paso 1 de 5</p>
            <h2 class="mt-1 text-2xl font-black text-slate-950">¿Para quién es este trabajo?</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">Identifica al cliente para encontrar la cotización fácilmente después.</p>
            <label class="mt-8 grid max-w-xl gap-2">
              <span class="label">Nombre del cliente</span>
              <input v-model="form.nombre_cliente" class="input py-3 text-base" autocomplete="name" placeholder="Ej. María Fernández" required autofocus />
              <span class="helper">Puede ser una persona, empresa o nombre del proyecto.</span>
            </label>
          </section>

          <section v-else-if="paso === 2">
            <p class="text-sm font-bold text-alvid">Paso 2 de 5</p>
            <h2 class="mt-1 text-2xl font-black text-slate-950">¿Qué vamos a fabricar?</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">Selecciona el tipo de mueble y describe lo que necesita el cliente.</p>
            <div class="mt-7 grid grid-cols-2 gap-3 sm:grid-cols-4">
              <button v-for="tipo in tiposMueble" :key="tipo" class="rounded-xl border p-3 text-left text-sm font-bold transition-all hover:-translate-y-0.5 hover:shadow-md" :class="form.tipo_mueble === tipo ? 'border-alvid bg-alvid-50 text-alvid ring-2 ring-alvid/10' : 'border-slate-200 bg-white text-slate-600'" type="button" @click="form.tipo_mueble = tipo">{{ tipo }}</button>
            </div>
            <label class="mt-6 grid gap-2">
              <span class="label">Descripción del trabajo</span>
              <textarea v-model="form.descripcion" class="input min-h-32 resize-y" placeholder="Ej. Ropero de dos cuerpos, tres cajones y espacio para colgar ropa..." required />
              <span class="helper">Incluye detalles útiles como cajones, puertas, divisiones o acabados.</span>
            </label>
          </section>

          <section v-else-if="paso === 3">
            <p class="text-sm font-bold text-alvid">Paso 3 de 5</p>
            <h2 class="mt-1 text-2xl font-black text-slate-950">Elige el material principal</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">El precio se estimará usando el costo y tamaño del tablero seleccionado.</p>
            <div v-if="materialesStore.cargando" class="mt-7 grid gap-3 sm:grid-cols-2"><div v-for="i in 4" :key="i" class="skeleton h-28" /></div>
            <div v-else class="mt-7 grid gap-3 sm:grid-cols-2">
              <label v-for="material in materialesStore.materiales" :key="material.id" class="cursor-pointer rounded-2xl border p-4 transition-all hover:-translate-y-0.5 hover:shadow-md" :class="Number(form.material_id) === material.id ? 'border-alvid bg-alvid-50 ring-2 ring-alvid/10' : 'border-slate-200 bg-white'">
                <input v-model="form.material_id" class="sr-only" type="radio" :value="material.id" />
                <div class="flex items-start justify-between gap-3">
                  <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-alvid shadow-sm"><Package :size="20" /></span>
                  <span class="badge" :class="material.stock <= 5 ? 'bg-red-100 text-red-700' : material.stock <= 10 ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'">{{ material.stock }} en stock</span>
                </div>
                <p class="mt-4 font-black text-slate-900">{{ material.nombre }}</p>
                <p class="mt-1 text-xs text-slate-500">{{ material.largo_mm }} × {{ material.ancho_mm }} × {{ material.espesor_mm }} mm</p>
                <p class="mt-3 text-sm font-black text-alvid">{{ material.precio_unitario_bs.toFixed(2) }} Bs / tablero</p>
              </label>
            </div>
          </section>

          <section v-else-if="paso === 4">
            <p class="text-sm font-bold text-alvid">Paso 4 de 5</p>
            <h2 class="mt-1 text-2xl font-black text-slate-950">Ingresa las medidas generales</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">Usa milímetros. Mide largo, profundidad y altura exterior del mueble.</p>
            <div class="mt-7 grid gap-4 sm:grid-cols-2">
              <label class="grid gap-2"><span class="label">Largo <span class="font-normal text-slate-400">(mm)</span></span><input v-model.number="form.largo_mm" class="input py-3 text-base font-bold" min="1" type="number" required /><span class="helper">De izquierda a derecha.</span></label>
              <label class="grid gap-2"><span class="label">Ancho / profundidad <span class="font-normal text-slate-400">(mm)</span></span><input v-model.number="form.ancho_mm" class="input py-3 text-base font-bold" min="1" type="number" required /><span class="helper">De frente hacia el fondo.</span></label>
              <label class="grid gap-2"><span class="label">Alto <span class="font-normal text-slate-400">(mm)</span></span><input v-model.number="form.alto_mm" class="input py-3 text-base font-bold" min="1" type="number" required /><span class="helper">Desde el piso hasta la parte superior.</span></label>
              <label class="grid gap-2"><span class="label">Cantidad de piezas</span><input v-model.number="form.cantidad_piezas" class="input py-3 text-base font-bold" min="1" type="number" required /><span class="helper">Paneles o partes estimadas del mueble.</span></label>
            </div>
          </section>

          <section v-else>
            <p class="text-sm font-bold text-alvid">Paso 5 de 5</p>
            <h2 class="mt-1 text-2xl font-black text-slate-950">Revisa y confirma la cotización</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">Puedes ajustar el precio final antes de guardar.</p>

            <div class="mt-7 grid gap-4 rounded-2xl border border-slate-200 bg-slate-50 p-5 sm:grid-cols-2">
              <div><p class="text-xs font-bold text-slate-500">Cliente</p><p class="mt-1 text-sm font-black text-slate-900">{{ form.nombre_cliente }}</p></div>
              <div><p class="text-xs font-bold text-slate-500">Mueble</p><p class="mt-1 text-sm font-black text-slate-900">{{ form.tipo_mueble }}</p></div>
              <div><p class="text-xs font-bold text-slate-500">Material</p><p class="mt-1 text-sm font-black text-slate-900">{{ materialSeleccionado?.nombre }}</p></div>
              <div><p class="text-xs font-bold text-slate-500">Medidas</p><p class="mt-1 text-sm font-black text-slate-900">{{ form.largo_mm }} × {{ form.ancho_mm }} × {{ form.alto_mm }} mm</p></div>
            </div>

            <div class="mt-5 grid gap-4 sm:grid-cols-[1fr_auto] sm:items-end">
              <label class="grid gap-2"><span class="label">Precio final (Bs)</span><input v-model.number="form.precio_final_bs" class="input py-3 text-lg font-black text-alvid" min="1" type="number" @input="precioFinalEditado = true" /><span class="helper">El valor es editable para aplicar descuentos o ajustes comerciales.</span></label>
              <button class="btn-secondary sm:mb-6" type="button" :disabled="prediciendo" @click="predecir"><Sparkles :size="18" />{{ prediciendo ? 'Calculando...' : 'Recalcular' }}</button>
            </div>
          </section>
        </div>

        <div v-if="error" class="alert-error mt-5" role="alert"><AlertCircle :size="20" class="shrink-0" />{{ error }}</div>

        <div class="mt-7 flex items-center justify-between border-t border-slate-100 pt-5">
          <button class="btn-secondary" type="button" :disabled="paso === 1" @click="anterior"><ArrowLeft :size="18" /> Atrás</button>
          <button v-if="paso < 5" class="btn-primary" type="button" @click="siguiente">Continuar <ArrowRight :size="18" /></button>
          <button v-else class="btn-primary" type="submit" :disabled="guardando || prediciendo"><span v-if="guardando" class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />{{ guardando ? 'Guardando...' : 'Guardar cotización' }}</button>
        </div>
      </form>
    </section>

    <aside class="grid content-start gap-4 xl:sticky xl:top-8">
      <ResumenCotizacion :prediccion="prediccion" :precio-final="form.precio_final_bs" compacto />
      <section class="panel p-5">
        <h3 class="text-sm font-black text-slate-900">Resumen del trabajo</h3>
        <dl class="mt-4 grid gap-3 text-sm">
          <div class="flex justify-between gap-4"><dt class="text-slate-500">Cliente</dt><dd class="max-w-[180px] truncate font-bold text-slate-800">{{ form.nombre_cliente || 'Sin definir' }}</dd></div>
          <div class="flex justify-between gap-4"><dt class="text-slate-500">Mueble</dt><dd class="font-bold text-slate-800">{{ form.tipo_mueble }}</dd></div>
          <div class="flex justify-between gap-4"><dt class="text-slate-500">Material</dt><dd class="max-w-[180px] truncate font-bold text-slate-800">{{ materialSeleccionado?.nombre || 'Sin definir' }}</dd></div>
          <div class="flex justify-between gap-4"><dt class="text-slate-500">Piezas</dt><dd class="font-bold text-slate-800">{{ form.cantidad_piezas }}</dd></div>
        </dl>
      </section>
    </aside>
  </div>
</template>

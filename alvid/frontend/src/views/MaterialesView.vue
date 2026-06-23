<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { AlertCircle, Boxes, Edit3, PackagePlus, Search, Trash2, TriangleAlert, X } from '@lucide/vue'

import { useMaterialesStore } from '../stores/materiales'

const store = useMaterialesStore()
const error = ref('')
const busqueda = ref('')
const formularioVisible = ref(false)
const porEliminar = ref(null)
const form = reactive({
  id: null,
  nombre: '',
  tipo: 'melamina',
  largo_mm: 2440,
  ancho_mm: 1830,
  espesor_mm: 18,
  precio_unitario_bs: 280,
  stock: 10
})

onMounted(() => store.cargarMateriales())

const materialesFiltrados = computed(() => store.materiales.filter((material) => `${material.nombre} ${material.tipo}`.toLowerCase().includes(busqueda.value.toLowerCase().trim())))
const stockTotal = computed(() => store.materiales.reduce((total, material) => total + material.stock, 0))
const stockCritico = computed(() => store.materiales.filter((material) => material.stock <= 5).length)

function limpiar() {
  Object.assign(form, { id: null, nombre: '', tipo: 'melamina', largo_mm: 2440, ancho_mm: 1830, espesor_mm: 18, precio_unitario_bs: 280, stock: 10 })
}

function abrirNuevo() {
  limpiar()
  formularioVisible.value = true
}

function editar(material) {
  Object.assign(form, material)
  formularioVisible.value = true
}

async function guardar() {
  error.value = ''
  try {
    await store.guardarMaterial({
      ...form,
      largo_mm: Number(form.largo_mm),
      ancho_mm: Number(form.ancho_mm),
      espesor_mm: Number(form.espesor_mm),
      precio_unitario_bs: Number(form.precio_unitario_bs),
      stock: Number(form.stock)
    })
    limpiar()
    formularioVisible.value = false
  } catch (err) {
    error.value = err.message
  }
}

async function confirmarEliminar() {
  if (!porEliminar.value) return
  error.value = ''
  try {
    await store.eliminarMaterial(porEliminar.value.id)
    porEliminar.value = null
  } catch (err) {
    error.value = err.message
  }
}

function stockClase(stock) {
  if (stock <= 5) return 'bg-red-100 text-red-700'
  if (stock <= 10) return 'bg-amber-100 text-amber-700'
  return 'bg-emerald-100 text-emerald-700'
}

function stockTexto(stock) {
  if (stock <= 5) return 'Stock crítico'
  if (stock <= 10) return 'Stock bajo'
  return 'Disponible'
}
</script>

<template>
  <div class="grid gap-6">
    <header class="flex flex-wrap items-end justify-between gap-4">
      <div><p class="text-sm font-bold text-alvid">Inventario</p><h1 class="page-title">Materiales</h1><p class="page-description">Controla existencias, medidas y precios de tus tableros.</p></div>
      <button class="btn-primary" type="button" @click="abrirNuevo"><PackagePlus :size="18" /> Nuevo material</button>
    </header>

    <div v-if="error || store.error" class="alert-error"><AlertCircle :size="20" />{{ error || store.error }}</div>

    <section class="grid gap-4 sm:grid-cols-3">
      <div class="panel flex items-center gap-4 p-5"><span class="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-100 text-blue-700"><Boxes :size="22" /></span><div><p class="text-2xl font-black text-slate-950">{{ store.materiales.length }}</p><p class="text-sm font-semibold text-slate-500">Tipos de material</p></div></div>
      <div class="panel flex items-center gap-4 p-5"><span class="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700"><PackagePlus :size="22" /></span><div><p class="text-2xl font-black text-slate-950">{{ stockTotal }}</p><p class="text-sm font-semibold text-slate-500">Unidades disponibles</p></div></div>
      <div class="panel flex items-center gap-4 p-5" :class="stockCritico ? 'border-red-200' : ''"><span class="flex h-11 w-11 items-center justify-center rounded-xl" :class="stockCritico ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-500'"><TriangleAlert :size="22" /></span><div><p class="text-2xl font-black text-slate-950">{{ stockCritico }}</p><p class="text-sm font-semibold text-slate-500">Con stock crítico</p></div></div>
    </section>

    <section class="panel p-4">
      <label class="relative block max-w-lg">
        <span class="sr-only">Buscar materiales</span>
        <Search :size="18" class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
        <input v-model="busqueda" class="input pl-11" placeholder="Buscar por nombre o tipo..." />
      </label>
    </section>

    <section v-if="store.cargando" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      <div v-for="i in 6" :key="i" class="panel p-5"><div class="skeleton h-10 w-10" /><div class="skeleton mt-5 h-5 w-48" /><div class="skeleton mt-3 h-4 w-32" /><div class="skeleton mt-6 h-10 w-full" /></div>
    </section>

    <section v-else-if="materialesFiltrados.length" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      <article v-for="material in materialesFiltrados" :key="material.id" class="panel group overflow-hidden transition-all hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-lg">
        <div class="p-5">
          <div class="flex items-start justify-between gap-3">
            <span class="flex h-11 w-11 items-center justify-center rounded-xl bg-alvid-50 text-alvid"><Boxes :size="22" /></span>
            <span class="badge" :class="stockClase(material.stock)"><span class="h-1.5 w-1.5 rounded-full bg-current" />{{ stockTexto(material.stock) }}</span>
          </div>
          <h2 class="mt-5 text-base font-black text-slate-900">{{ material.nombre }}</h2>
          <p class="mt-1 text-xs font-bold uppercase text-slate-400">{{ material.tipo }}</p>

          <div class="mt-5 grid grid-cols-2 gap-3 rounded-xl bg-slate-50 p-4">
            <div class="col-span-2"><p class="text-xs text-slate-500">Medidas del tablero</p><p class="mt-1 text-sm font-bold text-slate-800">{{ material.largo_mm }} × {{ material.ancho_mm }} × {{ material.espesor_mm }} mm</p></div>
            <div><p class="text-xs text-slate-500">Precio</p><p class="mt-1 text-sm font-black text-alvid">{{ material.precio_unitario_bs.toFixed(2) }} Bs</p></div>
            <div><p class="text-xs text-slate-500">Existencias</p><p class="mt-1 text-sm font-black text-slate-800">{{ material.stock }} unid.</p></div>
          </div>
        </div>
        <div class="flex border-t border-slate-100">
          <button class="flex flex-1 items-center justify-center gap-2 py-3 text-sm font-bold text-slate-600 transition hover:bg-slate-50 hover:text-alvid" type="button" @click="editar(material)"><Edit3 :size="16" /> Editar</button>
          <button class="flex flex-1 items-center justify-center gap-2 border-l border-slate-100 py-3 text-sm font-bold text-slate-600 transition hover:bg-red-50 hover:text-red-700" type="button" @click="porEliminar = material"><Trash2 :size="16" /> Eliminar</button>
        </div>
      </article>
    </section>

    <section v-else class="panel grid min-h-64 place-items-center p-8 text-center">
      <div><Boxes :size="38" class="mx-auto text-slate-300" /><h2 class="mt-4 text-base font-black">No hay materiales para mostrar</h2><p class="mt-1 text-sm text-slate-500">Cambia la búsqueda o registra un material nuevo.</p></div>
    </section>

    <div v-if="formularioVisible" class="fixed inset-0 z-[70] overflow-y-auto bg-slate-950/40 p-4 backdrop-blur-sm" @click.self="formularioVisible = false">
      <section class="ml-auto min-h-full w-full max-w-lg rounded-2xl bg-white p-5 shadow-2xl sm:p-7" role="dialog" aria-modal="true">
        <div class="flex items-start justify-between gap-4">
          <div><p class="text-sm font-bold text-alvid">{{ form.id ? 'Actualizar inventario' : 'Registrar inventario' }}</p><h2 class="mt-1 text-2xl font-black text-slate-950">{{ form.id ? 'Editar material' : 'Nuevo material' }}</h2></div>
          <button class="icon-button" type="button" aria-label="Cerrar" @click="formularioVisible = false"><X :size="19" /></button>
        </div>
        <form class="mt-7 grid gap-5" @submit.prevent="guardar">
          <label class="grid gap-2"><span class="label">Nombre del material</span><input v-model="form.nombre" class="input" placeholder="Ej. Melamina blanca 18 mm" required /></label>
          <label class="grid gap-2"><span class="label">Tipo</span><select v-model="form.tipo" class="input"><option value="tablero">Tablero</option><option value="madera">Madera</option><option value="MDF">MDF</option><option value="melamina">Melamina</option></select></label>
          <fieldset><legend class="label mb-2">Medidas en milímetros</legend><div class="grid grid-cols-3 gap-3"><label class="grid gap-1"><span class="helper">Largo</span><input v-model.number="form.largo_mm" class="input" type="number" min="1" required /></label><label class="grid gap-1"><span class="helper">Ancho</span><input v-model.number="form.ancho_mm" class="input" type="number" min="1" required /></label><label class="grid gap-1"><span class="helper">Espesor</span><input v-model.number="form.espesor_mm" class="input" type="number" min="1" required /></label></div></fieldset>
          <div class="grid grid-cols-2 gap-3"><label class="grid gap-2"><span class="label">Precio unitario (Bs)</span><input v-model.number="form.precio_unitario_bs" class="input" type="number" min="1" required /></label><label class="grid gap-2"><span class="label">Stock actual</span><input v-model.number="form.stock" class="input" type="number" min="0" required /></label></div>
          <div v-if="error" class="alert-error"><AlertCircle :size="20" />{{ error }}</div>
          <div class="mt-2 flex justify-end gap-3"><button class="btn-secondary" type="button" @click="formularioVisible = false">Cancelar</button><button class="btn-primary" type="submit">{{ form.id ? 'Guardar cambios' : 'Registrar material' }}</button></div>
        </form>
      </section>
    </div>

    <div v-if="porEliminar" class="fixed inset-0 z-[80] grid place-items-center bg-slate-950/40 p-4 backdrop-blur-sm" @click.self="porEliminar = null">
      <section class="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl"><div class="flex h-11 w-11 items-center justify-center rounded-xl bg-red-100 text-red-700"><Trash2 :size="22" /></div><h2 class="mt-5 text-xl font-black">¿Eliminar este material?</h2><p class="mt-2 text-sm leading-6 text-slate-600">Se eliminará <strong>{{ porEliminar.nombre }}</strong> del inventario. La operación puede fallar si ya está usado en cotizaciones.</p><div class="mt-6 flex justify-end gap-3"><button class="btn-secondary" @click="porEliminar = null">Cancelar</button><button class="btn-danger bg-red-600 text-white" @click="confirmarEliminar">Sí, eliminar</button></div></section>
    </div>
  </div>
</template>

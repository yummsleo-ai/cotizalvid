<script setup>
import { useRouter } from 'vue-router'

import FormularioCotizacion from '../components/FormularioCotizacion.vue'

const router = useRouter()

function guardada() {
  router.push({ name: 'cotizaciones' })
}
</script>

<template>
  <div class="grid gap-6">
    <div>
      <p class="text-sm font-bold text-alvid">Nuevo presupuesto</p>
      <h1 class="page-title">Crear cotización</h1>
      <p class="page-description">Sigue los pasos para preparar un precio claro y completo.</p>
    </div>
    <FormularioCotizacion @guardada="guardada" />
  </div>
</template>

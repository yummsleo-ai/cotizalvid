<script setup>
import { ArrowLeft, Home } from '@lucide/vue'
</script>

<template>
  <div class="grid min-h-[70vh] place-items-center">
    <section class="max-w-lg text-center">
      <span class="mx-auto flex h-32 w-32 items-center justify-center rounded-2xl bg-white p-2 shadow-lg">
        <img src="/logo-alvid.png" alt="ALVID" class="h-full w-full object-contain" />
      </span>
      <p class="mt-8 text-sm font-black uppercase text-alvid">Error 404</p>
      <h1 class="mt-2 text-3xl font-black text-slate-950">Esta página no está en el taller</h1>
      <p class="mt-3 text-sm leading-6 text-slate-600">La dirección puede estar incompleta o la pantalla ya no está disponible.</p>
      <div class="mt-7 flex flex-wrap justify-center gap-3">
        <button class="btn-secondary" type="button" @click="$router.back()"><ArrowLeft :size="18" /> Volver</button>
        <RouterLink class="btn-primary" to="/"><Home :size="18" /> Ir al inicio</RouterLink>
      </div>
    </section>
  </div>
</template>

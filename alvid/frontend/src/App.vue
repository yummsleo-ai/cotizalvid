<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import NavBar from './components/NavBar.vue'

const route = useRoute()
const mostrarNav = computed(() => route.name !== 'login')
</script>

<template>
  <div class="min-h-screen bg-[#f4f6f8]">
    <NavBar v-if="mostrarNav" />
    <main :class="mostrarNav ? 'min-h-screen min-w-0 px-4 pb-24 pt-20 sm:px-6 lg:ml-64 lg:px-8 lg:pb-10 lg:pt-8' : ''">
      <div :class="mostrarNav ? 'mx-auto min-w-0 w-full max-w-[1440px]' : ''">
      <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { AlertCircle, Check, Eye, EyeOff, LockKeyhole, Mail, ShieldCheck } from '@lucide/vue'

import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const error = ref('')
const mostrarPassword = ref(false)
const recordar = ref(true)
const ayudaVisible = ref(false)
const form = reactive({
  email: 'admin@alvid.com',
  password: 'alvid2024'
})

async function entrar() {
  error.value = ''
  ayudaVisible.value = false
  try {
    await auth.login(form, recordar.value)
    router.push({ name: 'dashboard' })
  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <main class="relative grid min-h-screen bg-[#eef2f5] lg:grid-cols-[minmax(420px,0.9fr)_minmax(560px,1.1fr)]">
    <section class="relative hidden overflow-hidden bg-alvid-900 p-12 text-white lg:flex lg:flex-col lg:justify-between">
      <div class="absolute inset-0 opacity-30" style="background-image: radial-gradient(circle at 20% 20%, #2e5d8d 0, transparent 32%), radial-gradient(circle at 90% 85%, #a86416 0, transparent 25%);" />
      <div class="relative flex items-center gap-3">
        <span class="flex h-20 w-20 items-center justify-center rounded-2xl bg-white p-1.5 shadow-lg">
          <img src="/logo-alvid.png" alt="Logo ALVID" class="h-full w-full object-contain" />
        </span>
        <div>
          <p class="text-2xl font-black">ALVID</p>
          <p class="text-sm text-blue-100">ERP para carpintería</p>
        </div>
      </div>

      <div class="relative max-w-xl">
        <p class="mb-5 inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-bold text-blue-50">
          <ShieldCheck :size="16" /> Gestión segura y centralizada
        </p>
        <h1 class="text-4xl font-black leading-tight">Tu taller, ordenado de principio a fin.</h1>
        <p class="mt-5 max-w-lg text-base leading-7 text-blue-100">Cotizaciones, materiales y planes de corte en una sola herramienta diseñada para trabajar con claridad.</p>

        <div class="mt-10 grid gap-4 sm:grid-cols-3">
          <div v-for="beneficio in ['Cotiza rápido', 'Controla stock', 'Optimiza cortes']" :key="beneficio" class="flex items-center gap-2 text-sm font-bold text-white">
            <span class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-400/20 text-emerald-300"><Check :size="14" /></span>
            {{ beneficio }}
          </div>
        </div>
      </div>

      <p class="relative text-xs text-blue-200">ALVID · Gestión profesional para trabajos de carpintería</p>
    </section>

    <section class="flex min-h-screen items-center justify-center px-5 py-10 sm:px-10">
      <div class="w-full max-w-md">
        <div class="mb-8 flex items-center gap-3 lg:hidden">
          <span class="flex h-16 w-16 items-center justify-center rounded-xl bg-white p-1 shadow-md">
            <img src="/logo-alvid.png" alt="Logo ALVID" class="h-full w-full object-contain" />
          </span>
          <div>
            <p class="text-xl font-black text-alvid">ALVID</p>
            <p class="text-xs font-semibold text-slate-500">ERP para carpintería</p>
          </div>
        </div>

        <div class="panel p-6 sm:p-8">
          <div class="mb-7">
            <p class="text-sm font-bold text-alvid">Bienvenido de nuevo</p>
            <h2 class="mt-1 text-2xl font-black text-slate-950">Ingresa a tu espacio de trabajo</h2>
            <p class="mt-2 text-sm leading-6 text-slate-500">Usa tus credenciales para continuar.</p>
          </div>

          <form class="grid gap-5" @submit.prevent="entrar">
            <label class="grid gap-2">
              <span class="label">Correo electrónico</span>
              <span class="relative">
                <Mail :size="18" class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input v-model="form.email" class="input pl-11" type="email" autocomplete="email" placeholder="nombre@empresa.com" required />
              </span>
            </label>

            <label class="grid gap-2">
              <span class="flex items-center justify-between gap-3">
                <span class="label">Contraseña</span>
                <button class="text-xs font-bold text-alvid hover:underline" type="button" @click="ayudaVisible = !ayudaVisible">¿Olvidaste tu contraseña?</button>
              </span>
              <span class="relative">
                <LockKeyhole :size="18" class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                <input v-model="form.password" class="input px-11" :type="mostrarPassword ? 'text' : 'password'" autocomplete="current-password" required />
                <button class="absolute right-2 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100" type="button" :aria-label="mostrarPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'" @click="mostrarPassword = !mostrarPassword">
                  <EyeOff v-if="mostrarPassword" :size="18" />
                  <Eye v-else :size="18" />
                </button>
              </span>
            </label>

            <label class="flex cursor-pointer items-center gap-3 text-sm font-semibold text-slate-600">
              <input v-model="recordar" class="h-4 w-4 rounded border-slate-300 text-alvid focus:ring-alvid" type="checkbox" />
              Recordar sesión en este equipo
            </label>

            <div v-if="ayudaVisible" class="rounded-xl border border-blue-200 bg-blue-50 p-3 text-sm leading-5 text-blue-800">
              Solicita al administrador de ALVID que restablezca tu acceso.
            </div>

            <div v-if="error || auth.error" class="alert-error" role="alert">
              <AlertCircle :size="20" class="mt-0.5 shrink-0" />
              <span>
                <strong class="block">No pudimos iniciar sesión</strong>
                <span class="font-normal">{{ error || auth.error }}</span>
              </span>
            </div>

            <button class="btn-primary mt-1 w-full py-3" type="submit" :disabled="auth.cargando">
              <span v-if="auth.cargando" class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
              {{ auth.cargando ? 'Verificando acceso...' : 'Ingresar a ALVID' }}
            </button>
          </form>
        </div>

        <p class="mt-5 text-center text-xs text-slate-500">Acceso exclusivo para personal autorizado de ALVID.</p>
      </div>
    </section>
  </main>
</template>

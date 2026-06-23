import { defineStore } from 'pinia'

import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('alvid_token') || sessionStorage.getItem('alvid_token'),
    usuario: JSON.parse(localStorage.getItem('alvid_usuario') || sessionStorage.getItem('alvid_usuario') || 'null'),
    cargando: false,
    error: ''
  }),
  getters: {
    autenticado: (state) => Boolean(state.token)
  },
  actions: {
    async login(credenciales, recordar = true) {
      this.cargando = true
      this.error = ''
      try {
        const { data } = await api.post('/auth/login', credenciales)
        this.token = data.access_token
        this.usuario = data.usuario
        const almacenamiento = recordar ? localStorage : sessionStorage
        const alternativo = recordar ? sessionStorage : localStorage
        alternativo.removeItem('alvid_token')
        alternativo.removeItem('alvid_usuario')
        almacenamiento.setItem('alvid_token', data.access_token)
        almacenamiento.setItem('alvid_usuario', JSON.stringify(data.usuario))
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.cargando = false
      }
    },
    logout() {
      this.token = null
      this.usuario = null
      localStorage.removeItem('alvid_token')
      localStorage.removeItem('alvid_usuario')
      sessionStorage.removeItem('alvid_token')
      sessionStorage.removeItem('alvid_usuario')
    }
  }
})

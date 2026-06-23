import { defineStore } from 'pinia'

import api from '../services/api'

export const useCotizacionesStore = defineStore('cotizaciones', {
  state: () => ({
    cotizaciones: [],
    resumen: null,
    cargando: false,
    error: ''
  }),
  actions: {
    async cargarCotizaciones() {
      this.cargando = true
      this.error = ''
      try {
        const { data } = await api.get('/cotizaciones/')
        this.cotizaciones = data
      } catch (error) {
        this.error = error.message
      } finally {
        this.cargando = false
      }
    },
    async cargarResumen() {
      const { data } = await api.get('/cotizaciones/resumen')
      this.resumen = data
      return data
    },
    async predecir(datos) {
      const { data } = await api.post('/cotizaciones/predecir', datos)
      return data
    },
    async crearCotizacion(datos) {
      const { data } = await api.post('/cotizaciones/', datos)
      this.cotizaciones.unshift(data)
      return data
    },
    async actualizarCotizacion(id, cambios) {
      const { data } = await api.put(`/cotizaciones/${id}`, cambios)
      const indice = this.cotizaciones.findIndex((cotizacion) => cotizacion.id === data.id)
      if (indice >= 0) this.cotizaciones[indice] = data
      return data
    },
    async eliminarCotizacion(id) {
      await api.delete(`/cotizaciones/${id}`)
      this.cotizaciones = this.cotizaciones.filter((cotizacion) => cotizacion.id !== id)
    },
    async generarPlanCorte(datos) {
      const { data } = await api.post('/cortes/generar', datos)
      return data
    }
  }
})

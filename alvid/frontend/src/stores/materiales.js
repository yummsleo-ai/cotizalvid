import { defineStore } from 'pinia'

import api from '../services/api'

export const useMaterialesStore = defineStore('materiales', {
  state: () => ({
    materiales: [],
    cargando: false,
    error: ''
  }),
  actions: {
    async cargarMateriales() {
      this.cargando = true
      this.error = ''
      try {
        const { data } = await api.get('/materiales/')
        this.materiales = data
      } catch (error) {
        this.error = error.message
      } finally {
        this.cargando = false
      }
    },
    async guardarMaterial(material) {
      if (material.id) {
        const { data } = await api.put(`/materiales/${material.id}`, material)
        const indice = this.materiales.findIndex((item) => item.id === data.id)
        if (indice >= 0) this.materiales[indice] = data
        return data
      }
      const { data } = await api.post('/materiales/', material)
      this.materiales.unshift(data)
      return data
    },
    async eliminarMaterial(id) {
      await api.delete(`/materiales/${id}`)
      this.materiales = this.materiales.filter((material) => material.id !== id)
    }
  }
})

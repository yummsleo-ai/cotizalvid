import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Agrega el JWT guardado a todas las solicitudes protegidas.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('alvid_token') || sessionStorage.getItem('alvid_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      return Promise.reject(new Error('No se pudo conectar con el servidor. Verifica que el backend esté iniciado.'))
    }
    const mensaje = error.response?.data?.detail || 'No se pudo completar la solicitud'
    return Promise.reject(new Error(Array.isArray(mensaje) ? 'Datos invalidos' : mensaje))
  }
)

export default api

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './style.css'

// Punto unico de montaje de la PWA.
createApp(App).use(createPinia()).use(router).mount('#app')

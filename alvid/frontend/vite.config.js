import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'ALVID',
        short_name: 'ALVID',
        description: 'Cotizaciones y planes de corte para carpinteria ALVID',
        theme_color: '#1F3864',
        background_color: '#F8FAFC',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: '/logo-alvid.png',
            sizes: '485x514',
            type: 'image/png',
            purpose: 'any maskable'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,ico}']
      }
    })
  ],
  server: {
    host: '0.0.0.0',
    port: 5173
  }
})

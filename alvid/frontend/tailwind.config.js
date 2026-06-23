export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        alvid: {
          DEFAULT: '#17365D',
          50: '#F0F5FA',
          100: '#DFEAF4',
          600: '#204A7A',
          700: '#17365D',
          800: '#102B4C',
          900: '#0B203A'
        },
        madera: '#A86416',
        exito: '#15803D'
      },
      boxShadow: {
        panel: '0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.05)'
      }
    }
  },
  plugins: []
}

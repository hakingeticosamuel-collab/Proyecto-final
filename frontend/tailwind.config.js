export default {
  content: ['./index.html', './src/**/*.{js,ts,vue}', './**/*.{vue,js}'],
  theme: {
    extend: {
      boxShadow: {
        'soft': '0 24px 80px rgba(15, 23, 42, 0.08)',
      },
      colors: {
        indigo: {
          950: '#10104d',
        },
      },
    },
  },
  plugins: [],
}

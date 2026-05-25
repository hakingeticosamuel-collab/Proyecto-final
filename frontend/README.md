# Paipa Smart Light Frontend

Interfaz Vue 3 + Tailwind CSS para el portal público de visualización.

## Estructura

- `App.vue` — página principal que usa `BaseLayout`, `MetricCard` y `ReportView`.
- `components/BaseLayout.vue` — layout con menú lateral colapsable y diseño responsive.
- `components/MetricCard.vue` — tarjetas KPI modernizadas.
- `components/ReportView.vue` — wrapper del iframe de Power BI con controles y skeleton loader.
- `main.js` — entrada de Vue.
- `tailwind.config.js` — configuración de Tailwind.
- `vite.config.js` — configuración de Vite.

## Cómo ejecutar

1. Instala dependencias:

```bash
cd frontend
npm install
```

2. Inicia el servidor de desarrollo:

```bash
npm run dev
```

3. Abre la URL indicada por Vite.

## Notas

- El componente `ReportView` encapsula el iframe de Power BI y muestra un skeleton loader mientras carga.
- El menú lateral del `BaseLayout` es mobile-first y se colapsa en pantallas pequeñas.
- Si no hay Node.js instalado, debes instalarlo primero para poder ejecutar el frontend.

<template>
  <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
    <div class="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
      <div>
        <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Leaflet.js</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Mapa interactivo del sistema</h2>
      </div>
      <p class="max-w-xl text-sm text-slate-600">El mapa muestra la zona de referencia del prototipo y puntos simbólicos para conectar IoT, operación y analítica de la entrega.</p>
    </div>

    <div ref="mapElement" class="mt-5 h-[420px] w-full rounded-[24px] border border-slate-200 bg-slate-100"></div>

    <div class="mt-5 grid gap-4 md:grid-cols-3">
      <div class="rounded-[20px] border border-slate-200 bg-slate-50 p-4">
        <p class="text-sm font-semibold text-slate-950">Paipa</p>
        <p class="mt-1 text-sm text-slate-600">Punto principal del prototipo de alumbrado.</p>
      </div>
      <div class="rounded-[20px] border border-slate-200 bg-slate-50 p-4">
        <p class="text-sm font-semibold text-slate-950">SQL Server / Somee</p>
        <p class="mt-1 text-sm text-slate-600">Origen operacional para pruebas y consulta.</p>
      </div>
      <div class="rounded-[20px] border border-slate-200 bg-slate-50 p-4">
        <p class="text-sm font-semibold text-slate-950">Power BI</p>
        <p class="mt-1 text-sm text-slate-600">Capa analítica para la visualización del DW.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const mapElement = ref(null)
let mapInstance = null

function createMarker(L, coordinates, title, description, color = '#0f172a') {
  const marker = L.circleMarker(coordinates, {
    radius: 9,
    color,
    weight: 2,
    fillColor: color,
    fillOpacity: 0.9,
  })

  marker.bindPopup(`<strong>${title}</strong><br>${description}`)
  return marker
}

onMounted(() => {
  if (!window.L || !mapElement.value) {
    return
  }

  const L = window.L
  mapInstance = L.map(mapElement.value, {
    scrollWheelZoom: false,
    zoomControl: true,
  }).setView([5.125, -73.118], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(mapInstance)

  // Default reference markers
  const defaults = [
    { lat: 5.125, lon: -73.118, title: 'Prototipo IoT', description: 'Ubicación referencial del sistema de alumbrado.', color: '#0f172a' },
    { lat: 5.129, lon: -73.105, title: 'SQL Server / Somee', description: 'Base operacional usada para pruebas y trazabilidad.', color: '#1d4ed8' },
    { lat: 5.119, lon: -73.129, title: 'Power BI', description: 'Capa analítica y visualización del DW.', color: '#7c3aed' },
  ]

  // Add default markers first
  defaults.forEach(d => createMarker(L, [d.lat, d.lon], d.title, d.description, d.color).addTo(mapInstance))

  // Try to fetch real markers from backend
  fetch('/api/markers')
    .then(r => r.ok ? r.json() : Promise.reject(r))
    .then(payload => {
      const markers = Array.isArray(payload) ? payload : payload.markers || []
      if (!markers.length) return
      // Clear default markers by removing and re-adding tiles (simple approach)
      // Add real markers
      markers.forEach(m => {
        if (!m || m.lat == null || m.lon == null) return
        createMarker(L, [Number(m.lat), Number(m.lon)], m.title || 'Ubicación', m.description || '', '#0b60ff').addTo(mapInstance)
      })
    })
    .catch(() => {
      // leave defaults on error
    })
})

onBeforeUnmount(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})
</script>
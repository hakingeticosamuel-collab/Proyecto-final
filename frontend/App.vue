<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm backdrop-blur-xl">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Resumen público</p>
        <h2 class="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Monitoreo de alumbrado inteligente</h2>
        <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600">
          Interfaz diseñada para exhibir el estado de la red de alumbrado, el reporte Power BI integrado y la georreferenciación en un estilo minimalista inspirado en Apple/Pixel.
        </p>
        <div v-if="apiError" class="mt-5 rounded-3xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {{ apiError }}
        </div>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Mediciones" :value="metrics.total_mediciones" description="Registros sincronizados con el Data Warehouse." />
      <MetricCard subtitle="Postes" :value="metrics.postes_activos" description="Ubicaciones activas en la ciudad de Paipa." />
      <MetricCard subtitle="Alertas" :value="metrics.alertas_activas" description="Eventos recientes que requieren atención." />
      <MetricCard subtitle="Consumo" :value="metrics.consumo_promedio.toFixed(2) + ' kWh'" description="Promedio de energía por lectura." />
    </template>

    <section id="dashboard" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Panel principal</p>
            <h2 class="mt-3 text-2xl font-semibold text-slate-950">Información sincronizada</h2>
            <p class="mt-2 text-sm leading-6 text-slate-600">Carga datos desde el backend y la API pública para mostrar el estado real del proyecto.</p>
          </div>

          <div class="grid gap-3 sm:auto-cols-max sm:grid-flow-col">
            <div class="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <label class="block text-xs uppercase tracking-[0.28em] text-slate-500">Periodo</label>
              <select v-model="selectedPeriod" @change="loadMetrics" class="mt-2 block w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-400">
                <option v-for="option in periodOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
              </select>
            </div>
            <button @click="loadMetrics" class="rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">Actualizar métricas</button>
          </div>
        </div>
      </div>

      <div class="grid gap-6 xl:grid-cols-[1.25fr_0.85fr]">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 class="text-lg font-semibold text-slate-950">Visión general</h3>
          <p class="mt-2 text-sm text-slate-600">Muestra los datos cargados desde los endpoints del backend y el almacén de datos.</p>
          <div class="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Mediciones</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.total_mediciones }}</p>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Postes</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.postes_activos }}</p>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Alertas</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.alertas_activas }}</p>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Consumo</p>
              <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.consumo_promedio.toFixed(2) }} kWh</p>
            </div>
          </div>
        </div>

        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <div class="flex items-center justify-between gap-4">
            <div>
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Top ubicaciones</p>
              <h3 class="mt-2 text-lg font-semibold text-slate-950">Ubicaciones más recientes</h3>
            </div>
            <button @click="loadLocations" class="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Actualizar</button>
          </div>
          <div class="mt-5 space-y-3">
            <div v-if="locations.length === 0" class="rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">No hay ubicaciones disponibles para mostrar.</div>
            <div v-else>
              <div v-for="location in locations.slice(0, 5)" :key="location.id" class="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                <div class="flex items-center justify-between gap-3">
                  <p class="text-base font-semibold text-slate-950">{{ location.name }}</p>
                  <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-600">{{ location.status }}</span>
                </div>
                <p class="mt-3 text-sm text-slate-600">Lat: {{ location.lat.toFixed(4) }}, Lng: {{ location.lng.toFixed(4) }}</p>
                <p class="mt-2 text-sm text-slate-600">Consumo: {{ location.consumo.toFixed(2) }} kWh</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="mapa" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Georreferenciación</p>
            <h2 class="mt-3 text-2xl font-semibold text-slate-950">Mapa de ubicaciones</h2>
            <p class="mt-2 text-sm leading-6 text-slate-600">Marcadores reales desde el DW, con estado, consumo y última medición por ubicación.</p>
          </div>
          <button @click="refreshMap" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Recargar ubicaciones</button>
        </div>
      </div>
      <div class="grid gap-6 xl:grid-cols-[1.45fr_0.85fr]">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Mapa interactivo</p>
              <h3 class="mt-2 text-xl font-semibold text-slate-950">Puntos reales en Paipa</h3>
            </div>
            <div class="flex flex-wrap gap-2 text-xs font-semibold uppercase tracking-[0.22em] text-slate-500">
              <span class="rounded-full bg-slate-100 px-3 py-2">Ubicaciones: {{ locations.length }}</span>
              <span class="rounded-full bg-rose-50 px-3 py-2 text-rose-700">Alertas: {{ reportSummary.alert_count }}</span>
              <span class="rounded-full bg-emerald-50 px-3 py-2 text-emerald-700">Con coordenadas: {{ reportSummary.locations_with_coordinates }}</span>
            </div>
          </div>
          <div ref="mapContainer" class="mt-5 h-[560px] rounded-[24px] border border-slate-200 bg-slate-100"></div>
          <p class="mt-4 text-sm text-slate-600">{{ mapStatus }}</p>
        </div>

        <div class="space-y-4">
          <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Resumen del DW</p>
            <div class="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
              <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Ubicaciones</p>
                <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.total_locations }}</p>
              </div>
              <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Mediciones</p>
                <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.measurement_count }}</p>
              </div>
              <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Alertas</p>
                <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.alert_count }}</p>
              </div>
              <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
                <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Consumo promedio</p>
                <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.average_consumption.toFixed(2) }} kWh</p>
              </div>
            </div>
          </div>

          <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
            <div class="flex items-center justify-between gap-3">
              <div>
                <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Top ubicaciones</p>
                <h3 class="mt-2 text-lg font-semibold text-slate-950">Mayor consumo</h3>
              </div>
              <button @click="loadReportSummary" class="rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Actualizar</button>
            </div>
            <div class="mt-4 space-y-3">
              <div v-if="topLocations.length === 0" class="rounded-[22px] border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">No hay datos de consumo para mostrar.</div>
              <div v-for="item in topLocations" :key="item.id" class="rounded-[22px] border border-slate-200 bg-slate-50 p-4">
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <p class="text-sm font-semibold text-slate-950">{{ item.name }}</p>
                    <p class="mt-1 text-xs uppercase tracking-[0.22em] text-slate-500">{{ item.status }}</p>
                  </div>
                  <span class="rounded-full bg-white px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-slate-600">{{ item.alert_count }} alertas</span>
                </div>
                <p class="mt-3 text-sm text-slate-600">Consumo: {{ item.consumo.toFixed(2) }} kWh</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="reportes" class="space-y-6">
      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Ubicaciones DW</p>
          <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.total_locations }}</p>
          <p class="mt-2 text-sm text-slate-600">Puntos registrados en el Data Warehouse.</p>
        </div>
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Coordenadas</p>
          <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.locations_with_coordinates }}</p>
          <p class="mt-2 text-sm text-slate-600">Ubicaciones listas para georreferenciación.</p>
        </div>
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Mediciones</p>
          <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.measurement_count }}</p>
          <p class="mt-2 text-sm text-slate-600">Lecturas almacenadas en dw.FactMediciones.</p>
        </div>
        <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Alertas</p>
          <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.alert_count }}</p>
          <p class="mt-2 text-sm text-slate-600">Eventos que requieren atención operativa.</p>
        </div>
      </div>

      <ReportView :src="powerBiUrl" @refresh="handleReportRefresh" />

      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">DW en tiempo reciente</p>
            <h2 class="mt-2 text-xl font-semibold text-slate-950">Últimas mediciones sincronizadas</h2>
          </div>
          <button @click="loadReportSummary" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Recargar</button>
        </div>
        <div class="mt-5 overflow-hidden rounded-[24px] border border-slate-200 bg-slate-50">
          <table class="min-w-full divide-y divide-slate-200 text-sm">
            <thead class="bg-slate-100">
              <tr>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Ubicación</th>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Fecha</th>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Consumo</th>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Alerta</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr v-if="recentMeasurements.length === 0">
                <td class="px-4 py-5 text-slate-600" colspan="4">No hay mediciones recientes disponibles.</td>
              </tr>
              <tr v-for="measurement in recentMeasurements" :key="`${measurement.post_id}-${measurement.measurement_date}`">
                <td class="px-4 py-4 text-slate-950">{{ measurement.location }}</td>
                <td class="px-4 py-4 text-slate-600">{{ formatDate(measurement.measurement_date) }}</td>
                <td class="px-4 py-4 text-slate-950">{{ measurement.consumo.toFixed(2) }} kWh</td>
                <td class="px-4 py-4 text-slate-600">{{ measurement.alert_status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Actividad reciente</p>
            <h2 class="mt-2 text-xl font-semibold text-slate-950">Registros recientes</h2>
          </div>
          <button @click="loadRecords" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Actualizar registros</button>
        </div>
        <div class="mt-5 overflow-hidden rounded-[24px] border border-slate-200 bg-slate-50">
          <table class="min-w-full divide-y divide-slate-200 text-sm">
            <thead class="bg-slate-100">
              <tr>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Dispositivo</th>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Fecha</th>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Valor</th>
                <th class="whitespace-nowrap px-4 py-3 text-left font-semibold uppercase tracking-[0.24em] text-slate-500">Estado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200">
              <tr v-if="records.length === 0">
                <td class="px-4 py-5 text-slate-600" colspan="4">No hay registros recientes. Usa el botón de actualizar.</td>
              </tr>
              <tr v-for="record in records.slice(0, 6)" :key="record.id">
                <td class="px-4 py-4 text-slate-950">{{ record.device_id }}</td>
                <td class="px-4 py-4 text-slate-600">{{ formatDate(record.measurement_date) }}</td>
                <td class="px-4 py-4 text-slate-950">{{ record.value }}</td>
                <td class="px-4 py-4 text-slate-600">{{ record.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </BaseLayout>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'
import ReportView from './components/ReportView.vue'

const selectedSection = ref('dashboard')
const selectedPeriod = ref('7d')
const periodOptions = [
  { value: '24h', label: 'Últimas 24 horas' },
  { value: '7d', label: 'Últimos 7 días' },
  { value: '30d', label: 'Último mes' },
]

const powerBiUrl = 'https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9'

const apiError = ref('')
const metrics = ref({
  total_mediciones: 0,
  postes_activos: 0,
  alertas_activas: 0,
  consumo_promedio: 0,
})
const locations = ref([])
const records = ref([])
const reportSummary = ref({
  total_locations: 0,
  locations_with_coordinates: 0,
  measurement_count: 0,
  alert_count: 0,
  average_consumption: 0,
})
const recentMeasurements = ref([])
const topLocations = ref([])
const mapStatus = ref('Cargando mapa interactivo...')
const mapContainer = ref(null)
const mapInstance = ref(null)
const markerLayer = ref(null)
const defaultMapCenter = [5.668, -73.1204]

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  return date.toLocaleString('es-CO', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

function buildPopup(location) {
  const lastMeasurement = location.last_measurement ? formatDate(location.last_measurement) : 'Sin dato reciente'
  return `
    <div style="min-width: 240px; line-height: 1.5;">
      <strong>${escapeHtml(location.name)}</strong><br />
      Estado: ${escapeHtml(location.status || 'Desconocido')}<br />
      Consumo: ${location.consumo.toFixed(2)} kWh<br />
      Promedio histórico: ${location.average_consumption.toFixed(2)} kWh<br />
      Alertas: ${location.alert_count}<br />
      Última medición: ${escapeHtml(lastMeasurement)}
    </div>`
}

async function ensureMap() {
  await nextTick()
  if (mapInstance.value || !mapContainer.value || !window.L) {
    return
  }

  mapInstance.value = window.L.map(mapContainer.value, {
    scrollWheelZoom: false,
  }).setView(defaultMapCenter, 13)

  window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(mapInstance.value)

  markerLayer.value = window.L.layerGroup().addTo(mapInstance.value)
}

async function syncMapMarkers() {
  await ensureMap()

  if (!mapInstance.value || !markerLayer.value) {
    mapStatus.value = 'El mapa no se pudo inicializar. Verifica que Leaflet esté disponible.'
    return
  }

  markerLayer.value.clearLayers()

  const validLocations = locations.value.filter((location) => Number.isFinite(location.lat) && Number.isFinite(location.lng) && location.lat !== 0 && location.lng !== 0)

  if (validLocations.length === 0) {
    mapInstance.value.setView(defaultMapCenter, 13)
    mapStatus.value = 'No hay ubicaciones con coordenadas válidas para mostrar.'
    return
  }

  const bounds = []
  validLocations.forEach((location) => {
    const coords = [location.lat, location.lng]
    const marker = window.L.circleMarker(coords, {
      radius: location.alert_count > 0 || String(location.status).toLowerCase().includes('alert') ? 10 : 8,
      color: location.alert_count > 0 || String(location.status).toLowerCase().includes('alert') ? '#be123c' : '#2563eb',
      weight: 2,
      fillColor: location.alert_count > 0 || String(location.status).toLowerCase().includes('alert') ? '#fb7185' : '#60a5fa',
      fillOpacity: 0.9,
    }).addTo(markerLayer.value)

    marker.bindPopup(buildPopup(location))
    bounds.push(coords)
  })

  mapInstance.value.fitBounds(bounds, { padding: [36, 36] })
  mapStatus.value = `${validLocations.length} marcadores cargados desde la base de datos.`
}

async function loadMetrics() {
  apiError.value = ''
  try {
    const response = await fetch(`/api/public/metrics?period=${selectedPeriod.value}`)
    if (!response.ok) {
      const body = await response.json().catch(() => null)
      throw new Error(body?.error || 'Error al cargar métricas')
    }
    const data = await response.json()
    metrics.value = {
      total_mediciones: data.total_mediciones || 0,
      postes_activos: data.postes_activos || 0,
      alertas_activas: data.alertas_activas || 0,
      consumo_promedio: data.consumo_promedio || 0,
    }
  } catch (error) {
    apiError.value = 'No fue posible cargar las métricas. Verifica la conexión con el backend.'
    console.error(error)
  }
}

async function loadLocations() {
  try {
    const response = await fetch('/api/public/locations')
    if (!response.ok) throw new Error('Error al cargar ubicaciones')
    locations.value = await response.json()
    await syncMapMarkers()
  } catch (error) {
    mapStatus.value = 'No fue posible cargar las ubicaciones del mapa.'
    console.error(error)
  }
}

async function loadReportSummary() {
  try {
    const response = await fetch('/api/public/report-summary')
    if (!response.ok) throw new Error('Error al cargar el resumen de reportes')
    const data = await response.json()
    reportSummary.value = data.summary || reportSummary.value
    recentMeasurements.value = data.recent_measurements || []
    topLocations.value = data.top_locations || []
  } catch (error) {
    console.error(error)
  }
}

async function loadRecords() {
  try {
    const response = await fetch('/api/public/records')
    if (!response.ok) throw new Error('Error al cargar registros')
    records.value = await response.json()
  } catch (error) {
    console.error(error)
  }
}

function handleNavigate(section) {
  selectedSection.value = section
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function handleReportRefresh() {
  loadMetrics()
  loadLocations()
  loadReportSummary()
  loadRecords()
}

function refreshMap() {
  loadLocations()
}

onMounted(() => {
  loadMetrics()
  loadLocations()
  loadReportSummary()
  loadRecords()
})

onBeforeUnmount(() => {
  if (mapInstance.value) {
    mapInstance.value.remove()
    mapInstance.value = null
    markerLayer.value = null
  }
})
</script>

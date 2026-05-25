<template>
  <div class="min-h-screen bg-slate-100 text-slate-900">
    <div class="border-b border-slate-200 bg-white shadow-sm">
      <div class="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div>
          <p class="text-sm font-semibold text-slate-950">Paipa Smart Light</p>
          <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Portal de visualización pública</p>
        </div>
        <nav class="flex flex-wrap items-center gap-2 text-sm text-slate-600">
          <button @click="scrollToSection('dashboard')" class="rounded-xl px-3 py-2 transition hover:bg-slate-100">Dashboard</button>
          <button @click="scrollToSection('mapa')" class="rounded-xl px-3 py-2 transition hover:bg-slate-100">Mapa</button>
          <button @click="scrollToSection('reportes')" class="rounded-xl px-3 py-2 transition hover:bg-slate-100">App</button>
          <button @click="goToDashboard" class="rounded-xl px-3 py-2 transition hover:bg-slate-100">Flask</button>
        </nav>
      </div>
    </div>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <section id="dashboard" class="space-y-6">
        <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Resumen público</p>
              <h2 class="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Monitoreo de alumbrado inteligente</h2>
              <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
                Vista pública del proyecto con datos sincronizados desde Somee, Power BI y el Data Warehouse.
              </p>
            </div>
            <div class="flex items-center gap-3">
              <button @click="loadMetrics" class="rounded-2xl bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800">Actualizar métricas</button>
              <button @click="goToDashboard" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Volver al dashboard</button>
            </div>
          </div>
          <div v-if="apiError" class="mt-5 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
            {{ apiError }}
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Mediciones</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.total_mediciones }}</p>
            <p class="mt-2 text-sm text-slate-600">Registros sincronizados con el Data Warehouse.</p>
          </div>
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Postes</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.postes_activos }}</p>
            <p class="mt-2 text-sm text-slate-600">Ubicaciones activas en la ciudad de Paipa.</p>
          </div>
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Alertas</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ metrics.alertas_activas }}</p>
            <p class="mt-2 text-sm text-slate-600">Eventos recientes que requieren atención.</p>
          </div>
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Consumo</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ formatNumber(metrics.consumo_promedio) }} kWh</p>
            <p class="mt-2 text-sm text-slate-600">Promedio de energía por lectura.</p>
          </div>
        </div>

        <div class="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
          <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Power BI</p>
                <h3 class="mt-2 text-xl font-semibold text-slate-950">Dashboard publicado</h3>
              </div>
            </div>
            <div class="mt-5 overflow-hidden rounded-2xl border border-slate-200 bg-slate-50">
              <iframe :src="powerBiUrl" title="Power BI Dashboard" class="h-[680px] w-full border-0"></iframe>
            </div>
          </div>

          <div class="space-y-4">
            <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Resumen del DW</p>
              <div class="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
                <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Ubicaciones</p>
                  <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.total_locations }}</p>
                </div>
                <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Mediciones</p>
                  <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.measurement_count }}</p>
                </div>
                <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Alertas</p>
                  <p class="mt-2 text-2xl font-semibold text-slate-950">{{ reportSummary.alert_count }}</p>
                </div>
                <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Consumo promedio</p>
                  <p class="mt-2 text-2xl font-semibold text-slate-950">{{ formatNumber(reportSummary.average_consumption) }} kWh</p>
                </div>
              </div>
            </div>

            <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Ubicaciones</p>
              <div class="mt-4 space-y-3">
                <div v-for="location in locations.slice(0, 4)" :key="location.id" class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-slate-950">{{ location.name }}</p>
                    <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-600">{{ location.status }}</span>
                  </div>
                  <p class="mt-2 text-sm text-slate-600">Consumo: {{ formatNumber(location.consumo) }} kWh</p>
                </div>
                <div v-if="locations.length === 0" class="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">No hay ubicaciones disponibles.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="mapa" class="mt-6 space-y-6">
        <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p class="text-sm uppercase tracking-[0.28em] text-slate-500">Georreferenciación</p>
              <h2 class="mt-2 text-2xl font-semibold text-slate-950">Mapa de ubicaciones</h2>
              <p class="mt-2 text-sm leading-6 text-slate-600">Marcadores reales desde el DW, con estado, consumo y última medición por ubicación.</p>
            </div>
            <button @click="refreshMap" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Recargar ubicaciones</button>
          </div>
        </div>
        <div class="grid gap-6 xl:grid-cols-[1.45fr_0.85fr]">
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
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
            <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Mayor consumo</p>
              <div class="mt-4 space-y-3">
                <div v-for="item in topLocations" :key="item.id" class="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <div class="flex items-start justify-between gap-3">
                    <div>
                      <p class="text-sm font-semibold text-slate-950">{{ item.name }}</p>
                      <p class="mt-1 text-xs uppercase tracking-[0.22em] text-slate-500">{{ item.status }}</p>
                    </div>
                    <span class="rounded-full bg-white px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-slate-600">{{ item.alert_count }} alertas</span>
                  </div>
                  <p class="mt-3 text-sm text-slate-600">Consumo: {{ formatNumber(item.consumo) }} kWh</p>
                </div>
                <div v-if="topLocations.length === 0" class="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">No hay datos de consumo para mostrar.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="reportes" class="mt-6 space-y-6">
        <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Ubicaciones DW</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.total_locations }}</p>
            <p class="mt-2 text-sm text-slate-600">Puntos registrados en el Data Warehouse.</p>
          </div>
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Coordenadas</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.locations_with_coordinates }}</p>
            <p class="mt-2 text-sm text-slate-600">Ubicaciones listas para georreferenciación.</p>
          </div>
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Mediciones</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.measurement_count }}</p>
            <p class="mt-2 text-sm text-slate-600">Lecturas almacenadas en dw.FactMediciones.</p>
          </div>
          <div class="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Alertas</p>
            <p class="mt-3 text-3xl font-semibold text-slate-950">{{ reportSummary.alert_count }}</p>
            <p class="mt-2 text-sm text-slate-600">Eventos que requieren atención operativa.</p>
          </div>
        </div>

        <ReportView :src="powerBiUrl" @refresh="handleReportRefresh" />

        <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
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
                  <td class="px-4 py-4 text-slate-950">{{ formatNumber(measurement.consumo) }} kWh</td>
                  <td class="px-4 py-4 text-slate-600">{{ measurement.alert_status }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Actividad reciente</p>
              <h2 class="mt-2 text-xl font-semibold text-slate-950">Timeline de registros Somee</h2>
            </div>
            <button @click="loadRecords" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Actualizar registros</button>
          </div>
          <div class="mt-5 grid gap-3 rounded-[24px] border border-slate-200 bg-slate-50 p-4 lg:grid-cols-4">
            <div>
              <label class="mb-2 block text-xs uppercase tracking-[0.24em] text-slate-500">Estado</label>
              <select v-model="recordFilters.status" @change="loadRecords" class="w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-400">
                <option value="">Todos</option>
                <option value="Activo">Activo</option>
                <option value="Inactivo">Inactivo</option>
              </select>
            </div>
            <div>
              <label class="mb-2 block text-xs uppercase tracking-[0.24em] text-slate-500">Dispositivo</label>
              <input v-model="recordFilters.device" @change="loadRecords" type="text" placeholder="Ej. Poste-01" class="w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
            </div>
            <div>
              <label class="mb-2 block text-xs uppercase tracking-[0.24em] text-slate-500">Fecha inicio</label>
              <input v-model="recordFilters.startDate" @change="loadRecords" type="date" class="w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
            </div>
            <div>
              <label class="mb-2 block text-xs uppercase tracking-[0.24em] text-slate-500">Fecha fin</label>
              <input v-model="recordFilters.endDate" @change="loadRecords" type="date" class="w-full rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-400" />
            </div>
          </div>

          <div class="mt-5 relative pl-6">
            <div class="absolute left-2 top-0 bottom-0 w-px bg-slate-200"></div>
            <div v-if="records.length === 0" class="rounded-[24px] border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">No hay registros recientes. Usa los filtros o actualiza los datos.</div>
            <div v-else class="space-y-4">
              <article
                v-for="record in records.slice(0, 8)"
                :key="record.id"
                class="relative rounded-[24px] border border-slate-200 bg-white p-4 pl-5 shadow-sm"
                :class="timelineCardClass(record.status)"
              >
                <span class="absolute -left-[13px] top-5 h-6 w-6 rounded-full border-4 border-white" :class="timelineDotClass(record.status)"></span>
                <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div class="space-y-2">
                    <div class="flex flex-wrap items-center gap-2">
                      <p class="text-base font-semibold text-slate-950">{{ record.device_id }}</p>
                      <span class="rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em]" :class="timelineBadgeClass(record.status)">{{ record.status }}</span>
                    </div>
                    <p class="text-sm text-slate-600">Medición: {{ formatDate(record.measurement_date) }}</p>
                    <p class="text-sm text-slate-600">Carga: {{ formatDate(record.created_at) }}</p>
                  </div>

                  <div class="rounded-3xl bg-slate-50 px-4 py-3 text-right">
                    <p class="text-xs uppercase tracking-[0.24em] text-slate-500">Valor destacado</p>
                    <p class="mt-1 text-3xl font-semibold text-slate-950">{{ formatNumber(record.value) }}</p>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, nextTick } from 'vue'
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
const recordFilters = ref({
  status: '',
  device: '',
  startDate: '',
  endDate: '',
})
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

function formatNumber(value, digits = 2) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(digits) : Number(0).toFixed(digits)
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
      consumo_promedio: Number(data.consumo_promedio) || 0,
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
    locations.value = (await response.json()).map((location) => ({
      ...location,
      lat: Number(location.lat) || 0,
      lng: Number(location.lng) || 0,
      consumo: Number(location.consumo) || 0,
      alert_count: Number(location.alert_count) || 0,
      average_consumption: Number(location.average_consumption) || 0,
    }))
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
    reportSummary.value = {
      ...reportSummary.value,
      ...(data.summary || {}),
      total_locations: Number(data.summary?.total_locations ?? reportSummary.value.total_locations) || 0,
      locations_with_coordinates: Number(data.summary?.locations_with_coordinates ?? reportSummary.value.locations_with_coordinates) || 0,
      measurement_count: Number(data.summary?.measurement_count ?? reportSummary.value.measurement_count) || 0,
      alert_count: Number(data.summary?.alert_count ?? reportSummary.value.alert_count) || 0,
      average_consumption: Number(data.summary?.average_consumption ?? reportSummary.value.average_consumption) || 0,
    }
    recentMeasurements.value = (data.recent_measurements || []).map((measurement) => ({
      ...measurement,
      consumo: Number(measurement.consumo) || 0,
    }))
    topLocations.value = (data.top_locations || []).map((item) => ({
      ...item,
      consumo: Number(item.consumo) || 0,
      alert_count: Number(item.alert_count) || 0,
    }))
  } catch (error) {
    console.error(error)
  }
}

async function loadRecords() {
  try {
    const params = new URLSearchParams()
    if (recordFilters.value.status) params.set('status', recordFilters.value.status)
    if (recordFilters.value.device) params.set('device', recordFilters.value.device)
    if (recordFilters.value.startDate) params.set('start_date', recordFilters.value.startDate)
    if (recordFilters.value.endDate) params.set('end_date', recordFilters.value.endDate)

    const query = params.toString()
    const response = await fetch(`/api/public/records${query ? `?${query}` : ''}`)
    if (!response.ok) throw new Error('Error al cargar registros')
    records.value = (await response.json()).map((record) => ({
      ...record,
      value: Number(record.value) || 0,
    }))
  } catch (error) {
    console.error(error)
  }
}

function timelineCardClass(status) {
  const normalized = String(status || '').toLowerCase()
  if (normalized === 'activo') return 'border-l-4 border-l-emerald-500'
  if (normalized === 'inactivo') return 'border-l-4 border-l-slate-400'
  return 'border-l-4 border-l-indigo-500'
}

function timelineDotClass(status) {
  const normalized = String(status || '').toLowerCase()
  if (normalized === 'activo') return 'bg-emerald-500'
  if (normalized === 'inactivo') return 'bg-slate-400'
  return 'bg-indigo-500'
}

function timelineBadgeClass(status) {
  const normalized = String(status || '').toLowerCase()
  if (normalized === 'activo') return 'bg-emerald-50 text-emerald-700'
  if (normalized === 'inactivo') return 'bg-slate-100 text-slate-600'
  return 'bg-indigo-50 text-indigo-700'
}

function scrollToSection(section) {
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function goToDashboard() {
  window.location.href = '/'
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
  nextTick(() => {
    scrollToSection('dashboard')
  })
})

onBeforeUnmount(() => {
  if (mapInstance.value) {
    mapInstance.value.remove()
    mapInstance.value = null
    markerLayer.value = null
  }
})
</script>

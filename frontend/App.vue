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
            <p class="mt-2 text-sm leading-6 text-slate-600">Muestra los puntos cargados del backend y su estado actual.</p>
          </div>
          <button @click="loadLocations" class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300">Recargar ubicaciones</button>
        </div>
      </div>
      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div v-if="locations.length === 0" class="col-span-full rounded-[28px] border border-slate-200 bg-slate-50 p-6 text-sm text-slate-600">No se encontraron ubicaciones. Usa el botón de actualizar para recargar.</div>
        <div v-for="location in locations.slice(0, 6)" :key="location.id" class="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
          <p class="text-xs uppercase tracking-[0.26em] text-slate-500">{{ location.name }}</p>
          <h3 class="mt-3 text-xl font-semibold text-slate-950">{{ location.status }}</h3>
          <div class="mt-4 space-y-2 text-sm text-slate-600">
            <p>Latitud: {{ location.lat.toFixed(5) }}</p>
            <p>Longitud: {{ location.lng.toFixed(5) }}</p>
            <p>Consumo: {{ location.consumo.toFixed(2) }} kWh</p>
          </div>
        </div>
      </div>
    </section>

    <section id="reportes" class="space-y-6">
      <ReportView :src="powerBiUrl" @refresh="handleReportRefresh" />
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
import { onMounted, ref } from 'vue'
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
  loadRecords()
}

onMounted(() => {
  loadMetrics()
  loadLocations()
  loadRecords()
})
</script>

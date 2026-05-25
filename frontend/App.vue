<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.32em] text-slate-400">Paipa Smart Light</p>
        <div class="mt-3 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div class="max-w-2xl">
            <h1 class="text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Portal público del proyecto</h1>
            <p class="mt-3 max-w-xl text-sm leading-7 text-slate-600 sm:text-base">Un sitio limpio y directo que muestra el proyecto Paipa Smart Light con datos públicos desde Somee/SQL Server y un dashboard Power BI embebido.</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <button class="rounded-full bg-slate-950 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-slate-800" @click="goTo('dashboard-publicado')">Ir al dashboard</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('mapa-interactivo')">Ir al mapa</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('datos-publicos')">Ver datos</button>
          </div>
        </div>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Mediciones" :value="summary.counts?.mediciones?.total_mediciones ?? '—'" description="Total de registros en dbo.medicion" />
      <MetricCard subtitle="Dispositivos" :value="summary.counts?.dispositivos?.total_dispositivos ?? '—'" description="Dispositivos activos en Somee" />
      <MetricCard subtitle="Última carga" :value="summary.counts?.fact_mediciones?.ultima_carga ?? '—'" description="Último lote cargado al DW" />
      <MetricCard subtitle="Conexión" :value="sourceLabel" description="Lectura pública desde Somee / SQL Server" />
    </template>

    <section id="introduccion" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Introducción</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Proyecto público Paipa Smart Light</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600">Este portal muestra el proyecto de alumbrado inteligente en Paipa con datos públicos de Somee/SQL Server, un dashboard Power BI embebido y un mapa interactivo de la solución.</p>
        <div class="mt-6 grid gap-4 sm:grid-cols-2">
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.26em] text-slate-400">Entrega</p>
            <p class="mt-2 text-lg font-semibold text-slate-950">Portal público</p>
            <p class="mt-1 text-sm text-slate-600">Presentación clara de datos, visualización y despliegue.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.26em] text-slate-400">Modo</p>
            <p class="mt-2 text-lg font-semibold text-slate-950">Lectura pública</p>
            <p class="mt-1 text-sm text-slate-600">Somee y el dashboard se muestran como contenido público verificado.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="datos-publicos" class="space-y-6">
      <SomeeCharts :chartData="chartData" />
    </section>

    <section id="dashboard-publicado" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Dashboard publicado</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Reporte embebido y métricas de lectura</h2>
        <div class="mt-4 grid gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(380px,1fr)]">
          <ReportView :reportUrl="sourceStatus.powerbi_url || ''" />
          <aside class="space-y-4">
            <div class="rounded-[24px] border border-slate-200 bg-white p-5 shadow-sm">
              <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Conexión Somee</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">{{ sourceLabel }}</p>
              <p class="mt-1 text-sm text-slate-600">{{ connectionDescription }}</p>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-white p-5 shadow-sm">
              <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Últimas mediciones</p>
              <div class="mt-3 space-y-3">
                <div v-for="row in latestMeasurements" :key="row.id_medicion" class="rounded-2xl bg-slate-50 p-3">
                  <div class="flex items-center justify-between gap-3">
                    <span class="font-medium text-slate-900">Sensor {{ row.id_sensor }}</span>
                    <span class="text-xs text-slate-400">{{ row.fuente }}</span>
                  </div>
                  <div class="mt-1 flex items-center justify-between gap-3 text-sm text-slate-600">
                    <span>{{ row.valor }}</span>
                    <span>{{ row.fecha_hora }}</span>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </section>

    <section id="mapa-interactivo" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-4 shadow-sm sm:p-6">
        <LeafletMap />
      </div>
    </section>
  </BaseLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'
import LeafletMap from './components/LeafletMap.vue'
import ReportView from './components/ReportView.vue'
import SomeeCharts from './components/SomeeCharts.vue'

const selectedSection = ref('introduccion')
const sourceStatus = ref({ source: 'Somee/SQL Server', configured: false, mode: 'unconfigured', powerbi_url: '' })
const summary = ref({ configured: false, counts: { mediciones: {}, dispositivos: {}, fact_mediciones: {} }, latest_mediciones: [] })
const latestMeasurements = ref([])
const chartData = ref({ daily_counts: [], sensor_counts: [] })

const dataAvailable = computed(() => {
  return (
    Number(summary.value.counts?.mediciones?.total_mediciones) > 0 ||
    Array.isArray(chartData.value.daily_counts) && chartData.value.daily_counts.length > 0 ||
    Array.isArray(chartData.value.sensor_counts) && chartData.value.sensor_counts.length > 0
  )
})

const sourceLabel = computed(() => {
  if (sourceStatus.value.configured) return 'Conectado en modo lectura'
  if (dataAvailable.value) return 'SQL Server disponible (Somee pendiente)'
  return 'Lectura Somee pendiente'
})

const connectionDescription = computed(() => {
  if (sourceStatus.value.configured) return 'La lectura está activa en modo solo consulta.'
  if (dataAvailable.value) return 'El sitio muestra datos SQL Server; falta la conexión pública Somee.'
  return 'Sin credenciales Somee; conexión pendiente.'
})

onMounted(async () => {
  try {
    const [statusResponse, summaryResponse, measurementsResponse] = await Promise.all([
      fetch('/api/source-status'),
      fetch('/api/summary'),
      fetch('/api/last-measurements'),
    ])

    if (statusResponse.ok) {
      const statusData = await statusResponse.json()
      sourceStatus.value = { ...sourceStatus.value, ...statusData }
    }

    if (summaryResponse.ok) {
      summary.value = await summaryResponse.json()
    }

    const chartsResponse = await fetch('/api/somee-charts')

    if (measurementsResponse.ok) {
      const measurementsData = await measurementsResponse.json()
      latestMeasurements.value = measurementsData.latest_mediciones || []
    }

    if (chartsResponse.ok) {
      const chartsData = await chartsResponse.json()
      chartData.value = chartsData || { daily_counts: [], sensor_counts: [] }
    }
  } catch {
    summary.value = { configured: false, counts: { mediciones: {}, dispositivos: {}, fact_mediciones: {} }, latest_mediciones: [] }
    latestMeasurements.value = []
    chartData.value = { daily_counts: [], sensor_counts: [] }
  }
})

function handleNavigate(section) {
  selectedSection.value = section
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function goTo(section) {
  handleNavigate(section)
}
</script>

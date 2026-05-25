<template>
  <div class="space-y-6">
    <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Gráficas Somee</p>
          <h2 class="mt-2 text-2xl font-semibold text-slate-950">Visualizaciones interactivas de los datos</h2>
        </div>
        <div class="flex items-center gap-3">
          <p class="max-w-xs text-xs leading-5 text-slate-500">Sincronización en tiempo real con Somee.</p>
          <button @click="buildCharts" class="rounded-full bg-slate-100 p-2 text-slate-600 hover:bg-slate-200 transition-colors" title="Actualizar gráficas">🔄</button>
        </div>
      </div>
      <div v-if="!hasRealData" class="mt-8 rounded-[24px] border border-amber-200 bg-amber-50 p-8 text-center text-sm text-slate-700">No se encontraron registros Somee reales; se muestra información de demostración para mantener la visualización.</div>
      <div class="mt-8 space-y-6">
        <div class="grid gap-4 md:grid-cols-3">
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Total de mediciones</p>
            <p class="mt-2 text-3xl font-semibold text-slate-950">{{ totalMediciones }}</p>
            <p class="mt-1 text-sm text-slate-600">Registros capturados desde Somee / SQL Server.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Sensores</p>
            <p class="mt-2 text-3xl font-semibold text-slate-950">{{ sensorCount }}</p>
            <p class="mt-1 text-sm text-slate-600">Sensores reportando datos en los últimos registros.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Última fecha</p>
            <p class="mt-2 text-3xl font-semibold text-slate-950">{{ lastDate }}</p>
            <p class="mt-1 text-sm text-slate-600">Último día con registros disponibles.</p>
          </div>
        </div>

        <div class="grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
          <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
            <div class="mb-4 flex items-center justify-between gap-4">
              <div>
                <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Tendencia</p>
                <h3 class="text-lg font-semibold text-slate-950">Mediciones por día</h3>
              </div>
              <span class="hidden rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-500 sm:inline">Interactivo</span>
            </div>
            <div class="relative h-[320px] w-full">
              <canvas ref="dailyChartCanvas"></canvas>
            </div>
          </div>

          <div class="space-y-4">
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Distribución</p>
              <h3 class="mt-2 text-lg font-semibold text-slate-950">Registros por sensor</h3>
              <div class="relative mt-5 h-[260px] w-full">
                <canvas ref="sensorChartCanvas"></canvas>
              </div>
            </div>
            <div class="rounded-[24px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Indicadores</p>
              <div class="mt-3 space-y-3 text-sm text-slate-600">
                <p><span class="font-semibold text-slate-900">{{ topSensor.name }}</span> tiene {{ topSensor.total }} registros.</p>
                <p>Los gráficos responden al conjunto real de registros Somee y mantienen la integridad visual de la web.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const props = defineProps({
  chartData: {
    type: Object,
    default: () => ({ daily_counts: [], sensor_counts: [] }),
  },
})

const dailyChartCanvas = ref(null)
const sensorChartCanvas = ref(null)
let dailyChart = null
let sensorChart = null

const hasRealData = computed(() => {
  return Array.isArray(props.chartData.daily_counts) && props.chartData.daily_counts.length > 0
})

const fallbackDailyCounts = [
  { dia: '2026-05-18', total_mediciones: 128 },
  { dia: '2026-05-19', total_mediciones: 142 },
  { dia: '2026-05-20', total_mediciones: 159 },
  { dia: '2026-05-21', total_mediciones: 173 },
  { dia: '2026-05-22', total_mediciones: 186 },
  { dia: '2026-05-23', total_mediciones: 194 },
  { dia: '2026-05-24', total_mediciones: 205 },
]

const fallbackSensorCounts = [
  { id_sensor: 'Sensor 1', total_registros: 78 },
  { id_sensor: 'Sensor 2', total_registros: 63 },
  { id_sensor: 'Sensor 3', total_registros: 49 },
  { id_sensor: 'Sensor 4', total_registros: 38 },
  { id_sensor: 'Sensor 5', total_registros: 24 },
]

const activeChartData = computed(() => {
  return hasRealData.value ? props.chartData : { daily_counts: fallbackDailyCounts, sensor_counts: fallbackSensorCounts }
})

const totalMediciones = computed(() => {
  return activeChartData.value.daily_counts.reduce((sum, row) => sum + Number(row.total_mediciones || 0), 0)
})

const sensorCount = computed(() => {
  return activeChartData.value.sensor_counts.length
})

const lastDate = computed(() => {
  const dates = activeChartData.value.daily_counts.map(row => row.dia).filter(Boolean)
  return dates.length ? dates[dates.length - 1] : '—'
})

const topSensor = computed(() => {
  if (!activeChartData.value.sensor_counts.length) return { name: '—', total: 0 }
  const top = activeChartData.value.sensor_counts.reduce((prev, current) => (+current.total_registros > +prev.total_registros ? current : prev), activeChartData.value.sensor_counts[0])
  return { name: top.id_sensor || 'Sensor', total: top.total_registros || 0 }
})

function destroyCharts() {
  if (dailyChart) {
    dailyChart.destroy()
    dailyChart = null
  }
  if (sensorChart) {
    sensorChart.destroy()
    sensorChart = null
  }
}

function buildCharts() {
  if (!window?.Chart) return
  destroyCharts()

  if (activeChartData.value.daily_counts.length && dailyChartCanvas.value) {
    const ctx = dailyChartCanvas.value.getContext('2d')
    dailyChart = new window.Chart(ctx, {
      type: 'line',
      data: {
        labels: activeChartData.value.daily_counts.map(row => row.dia),
        datasets: [
          {
            label: 'Mediciones por día',
            data: activeChartData.value.daily_counts.map(row => Number(row.total_mediciones || 0)),
            borderColor: '#1d4ed8',
            backgroundColor: 'rgba(59, 130, 246, 0.16)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 1500, easing: 'easeOutQuart' },
        plugins: {
          legend: { display: false },
          tooltip: { mode: 'index', intersect: false },
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#475569' } },
          y: { grid: { color: '#e2e8f0' }, ticks: { color: '#475569', beginAtZero: true } },
        },
      },
    })
  }

  if (activeChartData.value.sensor_counts.length && sensorChartCanvas.value) {
    const ctx = sensorChartCanvas.value.getContext('2d')
    sensorChart = new window.Chart(ctx, {
      type: 'bar',
      data: {
        labels: activeChartData.value.sensor_counts.map(row => row.id_sensor),
        datasets: [
          {
            label: 'Registros por sensor',
            data: activeChartData.value.sensor_counts.map(row => Number(row.total_registros || 0)),
            backgroundColor: '#2563eb',
            borderRadius: 8,
            barThickness: 22,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y}` } },
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#475569' } },
          y: { grid: { color: '#e2e8f0' }, ticks: { color: '#475569', beginAtZero: true } },
        },
      },
    })
  }
}

onMounted(buildCharts)
watch(() => props.chartData, buildCharts, { deep: true })
</script>

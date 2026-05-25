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
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('datos-publicos')">Ver gráficas</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('registros-datos')">Registros</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('conclusiones-alertas')">Conclusiones</button>
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
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Introducción y Funcionamiento</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Sistema Inteligente de Alumbrado</h2>
        <div class="mt-4 grid gap-8 md:grid-cols-2">
          <div>
            <h3 class="text-lg font-medium text-slate-900">¿Cómo funciona?</h3>
            <p class="mt-2 text-sm leading-7 text-slate-600">
              El sistema captura datos en tiempo real mediante nodos IoT (ESP32). Estos datos son enviados a una base de datos <strong>SQL Server (Somee)</strong>, procesados mediante un flujo ETL hacia un Data Warehouse y finalmente visualizados aquí mediante Power BI y gráficas nativas.
            </p>
          </div>
          <div>
            <h3 class="text-lg font-medium text-slate-900">Beneficios clave</h3>
            <ul class="mt-2 list-inside list-disc text-sm leading-7 text-slate-600">
              <li><strong>Eficiencia energética:</strong> Reducción de consumo mediante dimerización automática.</li>
              <li><strong>Mantenimiento preventivo:</strong> Detección de fallos en tiempo real.</li>
              <li><strong>Seguridad ciudadana:</strong> Iluminación dinámica según la presencia detectada.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section id="datos-publicos" class="space-y-6">
      <SomeeCharts :chartData="chartData" />
    </section>

    <section id="dashboard-publicado" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <div class="flex items-center justify-between gap-4">
          <div>
            <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Dashboard publicado</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-950">Reporte Power BI</h2>
          </div>
          <span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">Vista Completa</span>
        </div>
        <div class="mt-6 rounded-[24px] border border-slate-200 bg-white p-3 shadow-sm">
          <ReportView :reportUrl="sourceStatus.powerbi_url || ''" class="min-h-[550px] w-full" />
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-2">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
          <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Conexión Somee / SQL Server</p>
          <div class="mt-4 flex items-start gap-4">
            <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-blue-600">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-6 w-6"><path d="M4 7v10c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V7M4 7c0-1.1.9-2 2-2h12a2 2 0 0 1 2 2M4 7l8 5 8-5"/></svg>
            </div>
            <div>
              <p class="text-lg font-semibold text-slate-950">{{ sourceLabel }}</p>
              <p class="mt-1 text-sm leading-relaxed text-slate-600">{{ connectionDescription }}</p>
            </div>
          </div>
        </div>
        <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
          <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Actividad reciente</p>
          <div class="mt-4 space-y-3">
            <div v-for="row in latestMeasurements" :key="row.id_medicion" class="flex items-center justify-between rounded-2xl border border-slate-100 bg-slate-50/50 p-3">
              <div class="flex items-center gap-3">
                <div class="h-2 w-2 rounded-full bg-blue-500"></div>
                <span class="text-sm font-medium text-slate-900">Sensor {{ row.id_sensor }}</span>
              </div>
              <span class="text-sm font-semibold text-slate-950">{{ row.valor }}</span>
              <span class="text-xs text-slate-400 font-mono">{{ row.fecha_hora }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="registros-datos" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Explorador de Datos</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-950">Registros de Mediciones</h2>
          </div>
          <button @click="refreshTable" class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">Refrescar tabla</button>
        </div>
        <div class="mt-6 overflow-hidden rounded-[24px] border border-slate-200 bg-white shadow-sm">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
                <tr>
                  <th class="px-6 py-4 font-medium">ID</th>
                  <th class="px-6 py-4 font-medium">Sensor</th>
                  <th class="px-6 py-4 font-medium">Fecha/Hora</th>
                  <th class="px-6 py-4 font-medium">Valor</th>
                  <th class="px-6 py-4 font-medium">Calidad</th>
                  <th class="px-6 py-4 font-medium text-right">Fuente</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="row in tableData" :key="row.id_medicion" class="hover:bg-slate-50/50 transition-colors">
                  <td class="whitespace-nowrap px-6 py-4 font-medium text-slate-900">{{ row.id_medicion }}</td>
                  <td class="px-6 py-4 text-slate-600">Sensor {{ row.id_sensor }}</td>
                  <td class="px-6 py-4 text-slate-600">{{ row.fecha_hora }}</td>
                  <td class="px-6 py-4 font-semibold text-slate-950">{{ row.valor }}</td>
                  <td class="px-6 py-4">
                    <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold uppercase', row.calidad_dato === 'Buena' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700']">
                      {{ row.calidad_dato }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-right text-slate-400">{{ row.fuente }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <section id="conclusiones-alertas" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Resultados y Gestión</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Conclusiones y Alertas</h2>
        
        <div class="mt-8 grid gap-8 lg:grid-cols-2">
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-slate-900">Conclusiones del Proyecto</h3>
            <div class="space-y-3 text-sm leading-7 text-slate-600">
              <p>• <strong>Integración E2E:</strong> Se logró conectar con éxito el hardware IoT con SQL Server, procesos ETL y visualización avanzada en Power BI, cubriendo todo el ciclo del dato.</p>
              <p>• <strong>Toma de Decisiones:</strong> El Data Warehouse permite analizar patrones históricos de consumo, facilitando el mantenimiento preventivo del alumbrado público.</p>
              <p>• <strong>Escalabilidad:</strong> La arquitectura basada en Docker y Render permite que el portal sea accesible globalmente con alta disponibilidad para la supervisión ciudadana.</p>
            </div>
          </div>

          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-slate-900">Gestión de Alertas y Tiempos</h3>
            <div class="rounded-2xl bg-slate-50 p-5 shadow-inner">
              <div class="flex flex-col gap-6 sm:flex-row sm:items-center">
                <div class="flex-1">
                  <h4 class="text-sm font-bold text-slate-900 uppercase tracking-tight">Criterios de Alerta</h4>
                  <p class="mt-2 text-sm text-slate-600 italic">El sistema marca registros como "Alerta" automáticamente cuando:</p>
                  <ul class="mt-3 space-y-2 text-sm text-slate-600">
                    <li class="flex items-start gap-2">
                      <span class="text-amber-600 font-bold">●</span>
                      <span><strong>Fuera de Rango:</strong> El valor capturado excede los límites configurados para el sensor (Min/Max).</span>
                    </li>
                    <li class="flex items-start gap-2">
                      <span class="text-amber-600 font-bold">●</span>
                      <span><strong>Falla de Nodo:</strong> El dispositivo reporta un estado de error o pérdida de conectividad intermitente.</span>
                    </li>
                  </ul>
                </div>
                <div class="relative h-28 w-28 shrink-0">
                  <canvas ref="qualityChartCanvas"></canvas>
                  <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                    <span class="text-[10px] font-bold text-slate-400 uppercase leading-none">Calidad</span>
                  </div>
                </div>
              </div>
              <div class="mt-5 border-t border-slate-200 pt-4">
                <p class="text-xs font-semibold text-slate-400 uppercase">Frecuencia de Actualización (SLA)</p>
                <p class="mt-1 text-sm text-slate-600 font-medium font-mono">IoT: 60s | ETL: 15min | Power BI: Diario/Pro</p>
              </div>
            </div>
          </div>
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
import { computed, onMounted, ref, watch } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'
import LeafletMap from './components/LeafletMap.vue'
import ReportView from './components/ReportView.vue'
import SomeeCharts from './components/SomeeCharts.vue'

const selectedSection = ref('introduccion')
const sourceStatus = ref({ source: 'Somee/SQL Server', configured: false, mode: 'unconfigured', powerbi_url: '' })
const summary = ref({ configured: false, counts: { mediciones: {}, dispositivos: {}, fact_mediciones: {} }, latest_mediciones: [] })
const latestMeasurements = ref([])
const chartData = ref({ daily_counts: [], sensor_counts: [], quality_counts: [] })
const qualityChartCanvas = ref(null)
let qualityChart = null
const tableData = ref([])

const sourceLabel = computed(() => {
  if (sourceStatus.value.mode === 'read-only') return 'Somee conectado en modo lectura'
  if (sourceStatus.value.mode === 'error') return 'Credenciales Somee detectadas; error de conexión'
  return 'Sin credenciales Somee'
})

const connectionDescription = computed(() => {
  if (sourceStatus.value.mode === 'read-only') return 'La lectura está activa en modo solo consulta.'
  if (sourceStatus.value.mode === 'error') return sourceStatus.value.error ? `Error Somee: ${sourceStatus.value.error}` : 'Credenciales presentes, pero no se pudo conectar a Somee.'
  return 'No hay credenciales Somee. Introduce usuario y contraseña para activar la lectura pública.'
})

function buildQualityChart() {
  if (!window?.Chart || !qualityChartCanvas.value) return
  if (qualityChart) qualityChart.destroy()

  const data = chartData.value.quality_counts?.length 
    ? chartData.value.quality_counts 
    : [{ calidad: 'Buena', total: 80 }, { calidad: 'Alerta', total: 20 }]

  const ctx = qualityChartCanvas.value.getContext('2d')
  qualityChart = new window.Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.map(d => d.calidad),
      datasets: [{
        data: data.map(d => d.total),
        backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#6366f1'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '75%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label || '';
              const value = context.parsed;
              const total = context.dataset.data.reduce((acc, val) => acc + val, 0);
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
              return ` ${label}: ${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  })
}

async function fetchTableData() {
  try {
    const response = await fetch('/api/last-measurements?limit=20')
    if (response.ok) {
      const data = await response.json()
      tableData.value = data.latest_mediciones || []
    }
  } catch (error) {
    console.error('Error fetching table data:', error)
  }
}

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
      chartData.value = chartsData || { daily_counts: [], sensor_counts: [], quality_counts: [] }
    }
    buildQualityChart()

    await fetchTableData()
  } catch {
    summary.value = { configured: false, counts: { mediciones: {}, dispositivos: {}, fact_mediciones: {} }, latest_mediciones: [] }
    latestMeasurements.value = []
    chartData.value = { daily_counts: [], sensor_counts: [] }
    tableData.value = []
  }
})

watch(chartData, buildQualityChart, { deep: true })

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

function refreshTable() {
  fetchTableData()
}
</script>

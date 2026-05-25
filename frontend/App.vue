<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.32em] text-slate-400">Paipa Smart Light</p>
        <div class="mt-3 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div class="max-w-2xl">
            <h1 class="text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Portal público limpio para visualización y evidencia</h1>
            <p class="mt-3 max-w-xl text-sm leading-7 text-slate-600 sm:text-base">Una interfaz sobria para presentar la arquitectura del proyecto, el dashboard de Power BI, la lectura real de Somee y el mapa interactivo sin ruido técnico.</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <button class="rounded-full bg-slate-950 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-slate-800" @click="goTo('dashboard-publicado')">Ver dashboard</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('mapa-interactivo')">Ver mapa</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('publicacion-web')">Ver publicación</button>
          </div>
        </div>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Mediciones" :value="summary.counts?.mediciones?.total_mediciones ?? '—'" description="Total de registros en dbo.medicion" />
      <MetricCard subtitle="Dispositivos" :value="summary.counts?.dispositivos?.total_dispositivos ?? '—'" description="Dispositivos activos en Somee" />
      <MetricCard subtitle="Última carga" :value="summary.counts?.fact_mediciones?.ultima_carga ?? '—'" description="Último lote cargado al DW" />
      <MetricCard subtitle="Conexión" :value="sourceLabel" description="Estado real de la fuente Somee" />
    </template>

    <section id="portada" class="space-y-6">
      <div class="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Portada</p>
          <h2 class="mt-2 text-2xl font-semibold text-slate-950">Sistema Inteligente de Alumbrado Público — Paipa</h2>
          <p class="mt-3 text-sm leading-7 text-slate-600">Entrega 3: publicación web clara, con métricas de Somee, dashboard de Power BI y mapa interactivo para mostrar la relación entre IoT, analítica y ciudad inteligente.</p>
          <div class="mt-6 grid gap-4 sm:grid-cols-2">
            <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.26em] text-slate-400">Entrega</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">Portal público</p>
              <p class="mt-1 text-sm text-slate-600">Publicación web, prototipo, dashboard y sustentación.</p>
            </div>
            <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
              <p class="text-xs uppercase tracking-[0.26em] text-slate-400">Modo</p>
              <p class="mt-2 text-lg font-semibold text-slate-950">Lectura real</p>
              <p class="mt-1 text-sm text-slate-600">Somee se consulta solo en modo read-only.</p>
            </div>
          </div>
        </div>
        <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
          <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Ruta de presentación</p>
          <div class="mt-4 space-y-3">
            <div v-for="item in validationPoints" :key="item.title" class="rounded-[20px] border border-slate-200 bg-slate-50 p-4">
              <p class="text-sm font-semibold text-slate-950">{{ item.title }}</p>
              <p class="mt-1 text-sm text-slate-600">{{ item.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="introduccion" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Introducción</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Qué conecta este portal</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600">La experiencia une captura IoT, almacenamiento operacional en Somee/SQL Server, ETL, modelo analítico en DW, publicación con Flask y visualización en Power BI.</p>
      </div>
    </section>

    <section id="arquitectura" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Arquitectura</p>
            <h2 class="mt-2 text-2xl font-semibold text-slate-950">Flujo de datos de extremo a extremo</h2>
          </div>
          <span class="rounded-full bg-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-slate-600">IoT → SQL → ETL → DW → Power BI → Flask</span>
        </div>
        <div class="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div v-for="node in architectureNodes" :key="node.title" class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">{{ node.step }}</p>
            <p class="mt-3 text-lg font-semibold text-slate-950">{{ node.title }}</p>
            <p class="mt-2 text-sm text-slate-600">{{ node.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="prototipo-iot" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Prototipo IoT</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Dispositivos y captura</h2>
        <div class="mt-4 grid gap-4 lg:grid-cols-[1fr_0.8fr]">
          <div class="text-sm leading-7 text-slate-600">
            <p>La maqueta simula un sistema de alumbrado público con sensores de luminosidad, movimiento y consumo. Los datos se envían a SQL Server para luego alimentar el DW y el reporte analítico.</p>
            <div class="mt-4 flex flex-wrap gap-2">
              <span v-for="chip in iotChips" :key="chip" class="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{{ chip }}</span>
            </div>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Estado</p>
            <p class="mt-2 text-sm text-slate-600">La información mostrada en esta web se alinea con la evidencia del prototipo y la lectura real desde Somee cuando las credenciales están disponibles.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="publicacion-web" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Publicación web</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Render + Docker + Flask</h2>
        <div class="mt-4 grid gap-4 lg:grid-cols-[1fr_0.9fr]">
          <div class="space-y-3 text-sm leading-7 text-slate-600">
            <p>El portal se publica en Render con Docker. Flask sirve la SPA y expone las rutas de estado y lectura. La interfaz se mantiene simple y consistente para una presentación pública.</p>
            <p>La integración visual debe explicar IoT, Big Data, analítica y ciudades inteligentes sin recargar el panel con mensajes técnicos innecesarios.</p>
          </div>
          <div class="rounded-[22px] border border-slate-200 bg-slate-50 p-5">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Fuente</p>
            <p class="mt-2 text-sm font-medium text-slate-900">{{ sourceStatus.source }}</p>
            <p class="mt-1 text-sm text-slate-600">{{ sourceStatus.configured ? 'Conectado en modo de lectura' : 'Pendiente de credenciales' }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="dashboard-publicado" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Dashboard publicado</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Reporte embebido y métricas de lectura</h2>
        <div class="mt-4 grid gap-6 xl:grid-cols-[minmax(0,1.6fr)_minmax(280px,0.7fr)]">
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

    <section id="sustentacion" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Sustentación</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Cómo presentar el proyecto</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600">Recorre el flujo IoT, muestra el dashboard embebido, valida la lectura desde Somee y cierra con el mapa y las evidencias del despliegue.</p>
      </div>
    </section>

    <section id="demostracion-tecnica" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Demostración técnica</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Qué mostrar en vivo</h2>
        <ul class="mt-4 grid gap-3 text-sm text-slate-600 md:grid-cols-2">
          <li v-for="item in demoChecklist" :key="item" class="rounded-2xl bg-slate-50 p-4">{{ item }}</li>
        </ul>
      </div>
    </section>

    <section id="resultados" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Resultados</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Impacto y utilidad</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600">El sitio deja visible cómo los datos alimentan una visualización útil para ciudades inteligentes y cómo se publica de forma estable con Docker y Render.</p>
      </div>
    </section>

    <section id="conclusiones" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Conclusiones</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Cierre de la entrega</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600">La experiencia final debe sentirse pública, clara y verificable: Power BI visible, Somee conectado en lectura y navegación directa a cada parte del proyecto.</p>
      </div>
    </section>

    <section id="evidencias" class="space-y-6">
      <div class="rounded-[28px] border border-slate-200/80 bg-white/95 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.28em] text-slate-400">Evidencias</p>
        <h2 class="mt-2 text-2xl font-semibold text-slate-950">Capturas y pruebas</h2>
        <div class="mt-4 grid gap-4 md:grid-cols-3">
          <div v-for="evidence in evidenceCards" :key="evidence.title" class="rounded-[20px] border border-slate-200 bg-slate-50 p-3">
            <img :src="evidence.src" :alt="evidence.title" class="h-40 w-full rounded-[16px] object-cover" />
            <p class="mt-2 text-sm text-slate-600">{{ evidence.title }}</p>
          </div>
        </div>
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

const selectedSection = ref('portada')
const sourceStatus = ref({ source: 'Somee/SQL Server', configured: false, mode: 'unconfigured', powerbi_url: '' })
const summary = ref({ configured: false, counts: { mediciones: {}, dispositivos: {}, fact_mediciones: {} }, latest_mediciones: [] })
const latestMeasurements = ref([])

const sourceLabel = computed(() => (sourceStatus.value.configured ? 'Conectado' : 'Pendiente de credenciales'))
const connectionDescription = computed(() => (sourceStatus.value.configured ? 'La lectura está activa en modo solo consulta.' : 'Define las credenciales de entorno para activar la lectura real.'))

const validationPoints = [
  { title: '1. Contenedor', description: 'Vista reproducible con Docker y un único punto de entrada.' },
  { title: '2. UI', description: 'Layout claro, tipografía sobria y navegación por anclas internas.' },
  { title: '3. Datos', description: 'Somee/SQL Server en lectura, sin bloquear la carga si falla.' },
]

const architectureNodes = [
  { step: '1. IoT', title: 'Captura', description: 'Sensores y prototipo generan la evidencia operacional.' },
  { step: '2. SQL Server', title: 'Somee', description: 'Almacenamiento operacional para pruebas y validación.' },
  { step: '3. DW', title: 'ETL', description: 'Transformación y carga para analítica y reportes.' },
  { step: '4. Web', title: 'Flask + Power BI', description: 'Publicación visual y consulta de indicadores.' },
]

const iotChips = ['ESP32', 'BH1750', 'PIR', 'SCT-013', 'DS18B20']

const demoChecklist = [
  'Mostrar la portada y la navegación por secciones.',
  'Abrir el dashboard y validar el embed de Power BI.',
  'Comprobar la conexión Somee y las últimas mediciones.',
  'Moverse al mapa interactivo y revisar marcadores.',
  'Cerrar con evidencias y conclusiones del proyecto.',
]

const evidenceCards = [
  { title: 'Dashboard público', src: '/app/assets/images/evidence-dashboard.svg' },
  { title: 'Prototipo IoT', src: '/app/assets/images/evidence-prototype.svg' },
  { title: 'Despliegue', src: '/app/assets/images/evidence-deploy.svg' },
]

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

    if (measurementsResponse.ok) {
      const measurementsData = await measurementsResponse.json()
      latestMeasurements.value = measurementsData.latest_mediciones || []
    }
  } catch {
    summary.value = { configured: false, counts: { mediciones: {}, dispositivos: {}, fact_mediciones: {} }, latest_mediciones: [] }
    latestMeasurements.value = []
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

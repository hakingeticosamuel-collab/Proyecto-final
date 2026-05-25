<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-lg bg-white/80 p-6 shadow-sm">
        <h1 class="text-2xl font-semibold text-slate-900">Paipa Smart Light</h1>
        <p class="mt-2 text-sm text-slate-600 max-w-xl">Portal público minimalista para presentar el dashboard y métricas clave. Diseño inspirado en Apple/Pixel: mucho espacio, tipografía clara y acentos en índigo.</p>
      </div>
    </template>

    <template #cards>
      <div class="grid w-full grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-4">
        <MetricCard subtitle="Mediciones" :value="dataSummary.counts?.mediciones?.total_mediciones ?? '—'" description="Total de mediciones en la base" />
        <MetricCard subtitle="Dispositivos" :value="dataSummary.counts?.dispositivos?.total_dispositivos ?? '—'" description="Dispositivos registrados" />
        <MetricCard subtitle="Última medición" :value="dataSummary.counts?.mediciones?.ultima_medicion ?? '—'" description="Fecha última medición" />
        <MetricCard subtitle="DW carga" :value="dataSummary.counts?.fact_mediciones?.total_fact_mediciones ?? '—'" description="Registros en DW" />
      </div>
    </template>

    <section class="space-y-6">
      <div class="grid gap-6 lg:grid-cols-3">
        <div class="lg:col-span-2">
          <ReportView :reportUrl="sourceStatus.powerbi_url || ''" />
        </div>
        <aside class="space-y-4">
          <div class="rounded-lg bg-white/60 p-4">
            <p class="text-xs uppercase text-slate-500">Fuente de datos</p>
            <p class="mt-1 text-sm text-slate-700">{{ sourceStatus.source }} · <span class="font-medium">{{ sourceStatus.mode }}</span></p>
          </div>
          <div class="rounded-lg bg-white/60 p-4">
            <p class="text-xs uppercase text-slate-500">Últimas mediciones</p>
            <ul class="mt-2 text-sm text-slate-600 space-y-1">
              <li v-for="row in dataSummary.latest_mediciones" :key="row.id_medicion">{{ row.id_sensor }} — {{ row.valor }} • {{ row.fecha_hora }}</li>
            </ul>
          </div>
        </aside>
      </div>

      <div>
        <LeafletMap />
      </div>
    </section>
  </BaseLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'
import LeafletMap from './components/LeafletMap.vue'
import ReportView from './components/ReportView.vue'

const selectedSection = ref('portada')
const sourceStatus = ref({ source: 'Somee/SQL Server', configured: false, mode: 'unconfigured' })
const dataSummary = ref({ configured: false, counts: {}, latest_mediciones: [] })

onMounted(async () => {
  try {
    const response = await fetch('/api/source-status')
    if (response.ok) {
      sourceStatus.value = await response.json()
    }
  } catch {
    sourceStatus.value = { source: 'Somee/SQL Server', configured: false, mode: 'offline' }
  }

  try {
    const response = await fetch('/api/dw-summary')
    if (response.ok) {
      dataSummary.value = await response.json()
    }
  } catch {
    dataSummary.value = { configured: false, counts: {}, latest_mediciones: [] }
  }
})

function handleNavigate(section) {
  selectedSection.value = section
  const element = document.getElementById(section)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>

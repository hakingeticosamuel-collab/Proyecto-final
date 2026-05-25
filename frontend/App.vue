<template>
  <BaseLayout :selectedSection="selectedSection" @navigate="handleNavigate">
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm sm:p-8">
        <p class="text-xs uppercase tracking-[0.32em] text-slate-400">Paipa Smart Light</p>
        <div class="mt-3 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div class="max-w-2xl">
            <h1 class="text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">Portal público limpio para visualización y evidencia</h1>
            <p class="mt-3 max-w-xl text-sm leading-7 text-slate-600 sm:text-base">Una interfaz sobria para exponer el dashboard, las métricas reales de Somee y el mapa interactivo sin ruido visual.</p>
          </div>
          <div class="flex flex-wrap gap-2">
            <button class="rounded-full bg-slate-950 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-slate-800" @click="goTo('dashboard-publicado')">Ver dashboard</button>
            <button class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-slate-300 hover:bg-slate-50" @click="goTo('mapa-interactivo')">Ver mapa</button>
          </div>
        </div>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Mediciones" :value="dataSummary.counts?.mediciones?.total_mediciones ?? '—'" description="Total de mediciones en la base" />
      <MetricCard subtitle="Dispositivos" :value="dataSummary.counts?.dispositivos?.total_dispositivos ?? '—'" description="Dispositivos registrados" />
      <MetricCard subtitle="Última carga" :value="dataSummary.counts?.fact_mediciones?.ultima_carga ?? '—'" description="Carga más reciente del DW" />
      <MetricCard subtitle="Fuente" :value="sourceStatus.mode ?? '—'" description="Estado de la conexión Somee" />
    </template>

    <section class="space-y-6">
      <div class="grid gap-6 xl:grid-cols-[minmax(0,1.5fr)_minmax(300px,0.7fr)]">
        <ReportView :reportUrl="sourceStatus.powerbi_url || ''" />
        <aside class="space-y-4">
          <div class="rounded-[24px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Conexión</p>
            <p class="mt-2 text-lg font-semibold text-slate-950">{{ sourceStatus.source }}</p>
            <p class="mt-1 text-sm text-slate-600">{{ sourceStatus.configured ? 'Conectado a Somee' : 'Pendiente de credenciales' }} · {{ sourceStatus.mode }}</p>
          </div>
          <div class="rounded-[24px] border border-slate-200/80 bg-white/90 p-5 shadow-sm">
            <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Últimas mediciones</p>
            <ul class="mt-3 space-y-3 text-sm text-slate-600">
              <li v-for="row in dataSummary.latest_mediciones" :key="row.id_medicion" class="rounded-2xl bg-slate-50 p-3">
                <div class="flex items-center justify-between gap-3">
                  <span class="font-medium text-slate-900">Sensor {{ row.id_sensor }}</span>
                  <span class="text-xs text-slate-400">{{ row.fuente }}</span>
                </div>
                <div class="mt-1 flex items-center justify-between gap-3">
                  <span>{{ row.valor }}</span>
                  <span class="text-xs text-slate-500">{{ row.fecha_hora }}</span>
                </div>
              </li>
            </ul>
          </div>
        </aside>
      </div>

      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-4 shadow-sm sm:p-6">
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

function goTo(section) {
  handleNavigate(section)
}
</script>

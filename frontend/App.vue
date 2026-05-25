<template>
  <BaseLayout>
    <template #hero>
      <div class="rounded-[28px] border border-slate-200/80 bg-white/90 p-6 shadow-sm backdrop-blur-xl">
        <p class="text-xs uppercase tracking-[0.3em] text-slate-500">Resumen público</p>
        <h2 class="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Monitoreo de alumbrado inteligente</h2>
        <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600">
          Interfaz diseñada para exhibir el estado de la red de alumbrado, el reporte Power BI integrado y la georreferenciación en un estilo minimalista inspirado en Apple/Pixel.
        </p>
      </div>
    </template>

    <template #cards>
      <MetricCard subtitle="Mediciones" :value="metrics.total_mediciones" description="Registros sincronizados con el Data Warehouse." />
      <MetricCard subtitle="Postes" :value="metrics.postes_activos" description="Ubicaciones activas en la ciudad de Paipa." />
      <MetricCard subtitle="Alertas" :value="metrics.alertas_activas" description="Eventos recientes que requieren atención." />
      <MetricCard subtitle="Consumo" :value="metrics.consumo_promedio.toFixed(2) + ' kWh'" description="Promedio de energía por lectura." />
    </template>

    <section id="reportes">
      <ReportView src="https://app.powerbi.com/view?r=eyJrIjoiNzUwY2EyOTUtNGZiZS00MTE3LThjYTUtZDk5ZWY4MTIwODA3IiwidCI6IjA3ZGE2N2EwLTFmNDMtNGU4Yy05NzdmLTVmODhiNjQ3MGVlNiIsImMiOjR9" />
    </section>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseLayout from './components/BaseLayout.vue'
import MetricCard from './components/MetricCard.vue'
import ReportView from './components/ReportView.vue'

const metrics = ref({
  total_mediciones: 0,
  postes_activos: 0,
  alertas_activas: 0,
  consumo_promedio: 0,
})

async function loadMetrics() {
  try {
    const response = await fetch('/api/public/metrics')
    if (!response.ok) throw new Error('Error al cargar métricas')
    const data = await response.json()
    metrics.value = {
      total_mediciones: data.total_mediciones || 0,
      postes_activos: data.postes_activos || 0,
      alertas_activas: data.alertas_activas || 0,
      consumo_promedio: data.consumo_promedio || 0,
    }
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadMetrics)
</script>

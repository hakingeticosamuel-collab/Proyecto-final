<template>
  <div ref="frameHost" class="w-full">
    <div class="mb-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Power BI</p>
        <h3 class="text-base font-semibold text-slate-900">Dashboard publicado</h3>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button :disabled="!hasReportUrl" @click="toggleFullscreen" class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40">Pantalla completa</button>
        <button :disabled="!hasReportUrl" @click="reload" class="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40">Recargar</button>
        <button :disabled="!hasReportUrl" @click="openReport" class="inline-flex items-center gap-2 rounded-full bg-slate-950 px-3 py-2 text-sm text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400">Abrir</button>
      </div>
    </div>

    <div class="relative overflow-hidden rounded-[24px] border border-slate-200 bg-white shadow-sm">
      <div v-if="!hasReportUrl" class="flex min-h-[360px] items-center justify-center p-8 text-center">
        <div class="max-w-sm space-y-3">
          <p class="text-xs uppercase tracking-[0.24em] text-slate-400">Power BI</p>
          <h4 class="text-lg font-semibold text-slate-900">Conecta la URL del reporte</h4>
          <p class="text-sm leading-6 text-slate-600">Define `POWER_BI_URL` en el entorno para mostrar el dashboard embebido. Mientras tanto, el diseño permanece limpio y sin controles inactivos.</p>
        </div>
      </div>
      <div v-else-if="loading" class="p-8">
        <div class="animate-pulse space-y-3">
          <div class="h-5 w-1/4 bg-slate-200 rounded"></div>
          <div class="h-72 bg-slate-100 rounded"></div>
        </div>
      </div>
      <iframe
        v-else
        :key="frameKey"
        :src="reportUrl"
        class="h-[480px] w-full bg-white md:h-[620px]"
        frameborder="0"
        loading="lazy"
        title="Power BI report"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
const props = defineProps({
  reportUrl: { type: String, required: true },
})
const loading = ref(true)
const frameKey = ref(0)
const frameHost = ref(null)
const hasReportUrl = computed(() => Boolean(props.reportUrl))

function openReport() {
  if (!hasReportUrl.value) return
  window.open(props.reportUrl, '_blank', 'noopener')
}

function reload() {
  if (!hasReportUrl.value) return
  loading.value = true
  frameKey.value += 1
  window.setTimeout(() => {
    loading.value = false
  }, 650)
}

async function toggleFullscreen() {
  if (!hasReportUrl.value) return
  if (!document.fullscreenElement && frameHost.value?.requestFullscreen) {
    await frameHost.value.requestFullscreen()
    return
  }

  if (document.exitFullscreen) {
    await document.exitFullscreen()
  }
}

onMounted(() => {
  window.setTimeout(() => {
    loading.value = false
  }, 700)
})
</script>

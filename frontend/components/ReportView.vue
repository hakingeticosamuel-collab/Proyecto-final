<template>
  <section class="rounded-[28px] border border-slate-200/80 bg-white/90 p-5 shadow-sm backdrop-blur-xl transition hover:-translate-y-0.5 sm:p-6">
    <div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p class="text-xs uppercase tracking-[0.28em] text-slate-500">Informe integrado</p>
        <h2 class="text-2xl font-semibold tracking-tight text-slate-950">Power BI Live Report</h2>
      </div>
      <div class="grid gap-3 sm:grid-flow-col sm:auto-cols-max">
        <button @click="handleExpand" type="button" class="inline-flex items-center justify-center rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
          <span class="mr-2 inline-flex h-4 w-4 items-center justify-center text-indigo-600">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-4 w-4">
              <path d="M4 4h6M4 4v6M20 20h-6M20 20v-6" />
            </svg>
          </span>
          Expandir
        </button>
        <button @click="refreshReport" type="button" class="inline-flex items-center justify-center rounded-2xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-700">
          <span class="mr-2 inline-flex h-4 w-4 items-center justify-center text-white">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-4 w-4">
              <path d="M3 12a9 9 0 1 1 3.94 7.59" />
              <path d="M3 5v4h4" />
            </svg>
          </span>
          Actualizar
        </button>
        <button @click="downloadReport" type="button" class="inline-flex items-center justify-center rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50">
          <span class="mr-2 inline-flex h-4 w-4 items-center justify-center text-slate-700">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-4 w-4">
              <path d="M12 5v14" />
              <path d="M5 12l7 7 7-7" />
            </svg>
          </span>
          Descargar
        </button>
      </div>
    </div>

    <div class="overflow-hidden rounded-[24px] border border-slate-200/80 bg-slate-50">
      <div v-if="isLoading" class="animate-pulse p-6">
        <div class="mb-4 h-4 w-1/3 rounded-full bg-slate-200"></div>
        <div class="mb-4 h-4 w-2/3 rounded-full bg-slate-200"></div>
        <div class="grid gap-4 md:grid-cols-3">
          <div class="h-24 rounded-3xl bg-slate-200"></div>
          <div class="h-24 rounded-3xl bg-slate-200"></div>
          <div class="h-24 rounded-3xl bg-slate-200"></div>
        </div>
      </div>
      <iframe
        v-show="!isLoading"
        :src="iframeSrc"
        class="h-[720px] w-full border-0"
        @load="handleLoaded"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    default: 'Reporte integrado',
  },
})

const emit = defineEmits(['refresh', 'download'])

const isLoading = ref(true)
const iframeSrc = ref(`${props.src}?_=${Date.now()}`)

watch(
  () => props.src,
  (value) => {
    iframeSrc.value = `${value}?_=${Date.now()}`
  }
)

function handleLoaded() {
  isLoading.value = false
}

function refreshReport() {
  isLoading.value = true
  iframeSrc.value = `${props.src}?_=${Date.now()}`
  emit('refresh')
}

function downloadReport() {
  emit('download')
  window.open(props.src, '_blank')
}

function handleExpand() {
  window.open(props.src, '_blank')
}
</script>

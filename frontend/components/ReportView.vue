<template>
  <div class="w-full">
    <div class="flex items-center justify-between gap-3 mb-3">
      <h3 class="text-base font-semibold text-slate-900">Dashboard</h3>
      <div class="flex items-center gap-2">
        <button @click="expand" class="inline-flex items-center gap-2 rounded-md bg-white/60 px-3 py-2 text-sm text-slate-700 shadow-sm hover:bg-white">Expandir</button>
        <button @click="reload" class="inline-flex items-center gap-2 rounded-md bg-white/60 px-3 py-2 text-sm text-slate-700 shadow-sm hover:bg-white">Actualizar</button>
        <a :href="reportUrl" target="_blank" rel="noopener" class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-3 py-2 text-sm text-white hover:bg-indigo-700">Abrir</a>
      </div>
    </div>

    <div class="relative rounded-lg border border-slate-100 bg-white overflow-hidden">
      <div v-if="loading" class="p-8">
        <div class="animate-pulse space-y-3">
          <div class="h-5 w-1/4 bg-slate-200 rounded"></div>
          <div class="h-72 bg-slate-100 rounded"></div>
        </div>
      </div>
      <iframe v-else :src="reportUrl" class="w-full h-[480px] bg-white" frameborder="0" loading="lazy"></iframe>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const props = defineProps({
  reportUrl: { type: String, required: true },
})
const loading = ref(true)

function expand() {
  window.open(props.reportUrl, '_blank')
}

function reload() {
  loading.value = true
  // small debounce to show loader
  setTimeout(() => (loading.value = false), 700)
}

onMounted(() => {
  // simulate iframe ready after short delay
  setTimeout(() => (loading.value = false), 900)
})
</script>

<style scoped>
.rounded-lg { border-radius: 12px; }
</style>
